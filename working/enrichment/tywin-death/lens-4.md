# LENS 4 — Existing-node ↔ Existing-node causal wiring (cross-arc seams)
# Unit: assassination-of-tywin-lannister
# Session: 2026-06-23

This lens finds edges where **both** endpoints already exist and no topic-lens
"owns" the seam. Every proposal confirms node existence via `graph-query.py
--neighbors` before proposing.

---

## EDGE PROPOSALS

---

### SEAM 1 — Elia's murder MOTIVATES Oberyn's decision to champion Tyrion

**SOURCE:** `murder-of-elia-martell-and-rhaegars-children`
**EDGE:** `MOTIVATES`
**TARGET:** `oberyn-martell`

**Node check:**
- `murder-of-elia-martell-and-rhaegars-children` — EXISTS (event.assassination)
- `oberyn-martell` — EXISTS (character.human)

**Existing graph state:** `murder-of-elia-martell-and-rhaegars-children MOTIVATES eddard-stark`
already exists. There is NO `murder-of-elia-martell-and-rhaegars-children MOTIVATES oberyn-martell`
edge in the graph. `oberyn-martell HATES gregor-clegane` exists, but the upstream
structural cause — that the murder is what drives Oberyn into the role of Tyrion's champion
— is missing.

**Grounded in text (asos-tyrion-09.md):** Oberyn visits Tyrion in his cell and explicitly
names the murder as his motivation for agreeing to be his champion and for taking the role
of judge:

> "There has been none for Elia, Aegon, or Rhaenys. Why should there be any for you?"
> — `asos-tyrion-09.md:399`

> "'Not as your judge. As your champion.'"
> — `asos-tyrion-09.md:419`

And in asos-tyrion-10.md, Oberyn repeats the litany during combat, making the causal link
fully explicit — he championed Tyrion in order to get Gregor alone and extract a
confession about Elia:

> "I am Oberyn Martell, a prince of Dorne," he said, as the Mountain turned to keep him in
> sight. "Princess Elia was my sister."
> — `asos-tyrion-10.md:187`

> "You raped her. You murdered her. You killed her children."
> — `asos-tyrion-10.md:191`

> "I came to hear you confess."
> — `asos-tyrion-10.md:195` (Oberyn, to Gregor)

**Tier:** Tier 1 (on-page motive, stated explicitly)
**Rationale:** The murder is the reason Oberyn is in King's Landing, the reason he lobbied
for the role of judge (to be present), and the reason he agreed to champion Tyrion — to
reach Gregor in single combat. This is the defining cross-arc seam: Roberts' Rebellion /
Sack-of-KL arc wires directly into the Tywin-death arc via Oberyn's motivation.

---

### SEAM 2 — Jaime's revelation about Tysha MOTIVATES Tyrion (already exists) PLUS: tywin-lannister DECEIVES tyrion-lannister (dyadic)

**SOURCE:** `tywin-lannister`
**EDGE:** `DECEIVES`
**TARGET:** `tyrion-lannister`

**Node check:**
- `tywin-lannister` — EXISTS (character.human)
- `tyrion-lannister` — EXISTS (character.human)

**Existing graph state:** No `tywin-lannister DECEIVES tyrion-lannister` dyadic edge exists.
`jaime-reveals-the-truth-of-tysha MOTIVATES tyrion-lannister` already captures the
revelation-trigger. What is missing is the upstream character-to-character dyadic: Tywin
fabricated the story that Tysha was a paid whore, told Jaime to lie about it, and
orchestrated the assault. This deception, sustained over decades, is part of the causal
chain that ends in Tywin's death.

**Grounded in text (asos-tyrion-11.md):**

> "She was no whore. I never bought her for you. That was a lie that Father commanded me
> to tell."
> — `asos-tyrion-11.md:79`

> "What did you do with Tysha?" … "Oh, yes. Your first whore." Tyrion took aim at his
> father's chest. "The next time you say that word, I'll kill you."
> — `asos-tyrion-11.md:241–243`

Tywin's own words confirm the deception was his: he told the lie, he enforced its
consequences ("given her to his guards"), and his final word — "Wherever whores go" —
triggers Tyrion's finger on the crossbow.

**Tier:** Tier 1 (on-page, Tywin commands the lie, Jaime confirms it)
**Rationale:** This is a clean dyadic seam: an existing character DECEIVES an existing
character, causally upstream of the assassination. The deceiver IS the victim. The existing
spine has the revelation-event but lacks the character-level deceiver tag.

---

### SEAM 3 — jaime-reveals-the-truth-of-tysha CAUSES tyrion-kills-shae-in-tywins-bed (already exists) — CONFIRM AND EXTEND: also CAUSES the assassination via the detour

**This edge already exists in the spine.** Confirmed — no re-proposal.

BUT the following RELATED seam is missing:

**SOURCE:** `tyrion-kills-shae-in-tywins-bed`
**EDGE:** `ENABLES`
**TARGET:** `assassination-of-tywin-lannister`

**Node check:**
- `tyrion-kills-shae-in-tywins-bed` — EXISTS (event.death)
- `assassination-of-tywin-lannister` — EXISTS (event.assassination)

**Existing graph state:** The spine wires `jaime-reveals-the-truth-of-tysha CAUSES
assassination-of-tywin-lannister` directly. But the actual sequence in chapter 11 is:
Tyrion climbs the secret passage → enters Tywin's bedchamber → strangles Shae → picks up
Tywin's crossbow from the wall → proceeds to the privy → shoots Tywin. The killing of
Shae in Tywin's bedchamber is the event that places Tyrion inside the Tower of the Hand
WITH the crossbow in hand. It is not a constitutive beat of the assassination, but it
ENABLES it: Tyrion would not have been physically positioned at the weapon, inside the
tower, without having made the side-trip to the bed.

**Grounded in text (asos-tyrion-11.md):**

> "Afterward he found Lord Tywin's dagger on the bedside table and shoved it through his
> belt. A lion-headed mace, a poleaxe, and a crossbow had been hung on the walls. … He
> climbed up, pulled down the bow and a leather quiver packed with quarrels, jammed a foot
> into the stirrup, and pushed down until the bowstring cocked."
> — `asos-tyrion-11.md:211`

Tyrion acquires the murder weapon (the crossbow) as a direct consequence of entering
Tywin's room, which he entered because of Shae. Without the Shae detour, he goes to the
river with Varys, unarmed.

**Tier:** Tier 2, `verified_by: pending`
**Rationale:** This is an ENABLES not a CAUSES — it is Tyrion's free choice that produces
the assassination, but the Shae event doors-opened the weapon-access. Mark conservatively
Tier 2 because the spine's `jaime-reveals-the-truth-of-tysha CAUSES assassination` already
covers the motivational causation; this is the *instrumental* enabling link.
**Agency-check:** No agency-collapse. Tyrion makes a free choice to go up the ladder and
then a second choice to continue to the privy; the Shae event enables but does not compel
either.

---

### SEAM 4 — Shae testifies at trial: shae BETRAYS tyrion-lannister (dyadic, trial testimony)

**Node check:**
- `shae` — EXISTS (character.human)
- `tyrion-lannister` — EXISTS (character.human)

**Existing graph state:** `shae BETRAYS tyrion-lannister` already appears TWICE in the
graph (refs: asos-tyrion-10.md:27 and asos-tyrion-11.md:203). Both are already captured.
**No new edge needed here.** Confirmed absent of gap.

---

### SEAM 5 — Oberyn's championing of Tyrion MOTIVATES oberyn-martell toward the assassination-of-tywin goal (cross-arc motive → gregor-confesses)

Already well-wired via the spine. The `gregor-confesses-and-kills-oberyn CAUSES
jaime-frees-tyrion-from-the-black-cells` chain handles this. No gap.

---

### SEAM 6 — jaime-frees-tyrion-from-the-black-cells CAUSES jaime-reveals-the-truth-of-tysha (already exists) — gap check: does JAIME's choice here BREAK a VOW?

**SOURCE:** `jaime-lannister`
**EDGE:** `BREAKS_VOW`
**TARGET:** `jaime-frees-tyrion-from-the-black-cells`

**Node check:**
- `jaime-lannister` — EXISTS (character.human)
- `jaime-frees-tyrion-from-the-black-cells` — EXISTS (event.incident)

**Existing graph state:** `jaime-lannister AGENT_IN jaime-frees-tyrion-from-the-black-cells`
already exists. No `jaime-lannister BREAKS_VOW jaime-frees-tyrion-from-the-black-cells`
exists.

**Assessment of the seam:** Freeing a condemned prisoner is a violation of the king's
justice and arguably of Jaime's oath of service to the realm. However, Tyrion is condemned
by Tywin (acting Hand) not by the king personally, and Jaime is not an officer of the
Watch or the court — he is Kingsguard, sworn to the king's person. The text treats this
as a debt/fraternal act, not framed by Jaime as oath-breaking:

> "It was . . . a debt I owed you." Jaime's voice was strange.
> — `asos-tyrion-11.md:63`

There is no explicit invocation of vow, oath, or duty-violation in the chapter. Jaime
frames this as a personal debt, not a rupture with any sworn obligation. The BREAKS_VOW
edge would be an inferential over-read. **REJECTED** — see Self-Rejected section below.

---

### SEAM 7 — jaime-reveals-the-truth-of-tysha CAUSES tyrion-lannister SEEKS tysha (cross-arc: the Essos arc)

**SOURCE:** `jaime-reveals-the-truth-of-tysha`
**EDGE:** `CAUSES`
**TARGET:** `tyrion-lannister SEEKS tysha`

**Note:** The graph already has `tyrion-lannister SEEKS tysha` (ref: adwd-tyrion-06.md:15).
The missing edge is: does the revelation event CAUSE this seeking?

**Existing graph state:** `jaime-reveals-the-truth-of-tysha MOTIVATES tyrion-lannister`
exists. `tyrion-lannister SEEKS tysha` exists (via ADWD). No edge wiring the revelation
event to the seeking behavior.

**Grounded in text:** The revelation is on-page in asos-tyrion-11.md. Tyrion's seeking in
ADWD is the downstream consequence. The motivational chain is: revelation → rage/grief →
"wherever whores go" → crossbow → exile → river → Essos → Tyrion seeks Tysha. The
revelation in asos-tyrion-11 is the direct upstream cause of the ADWD seeking.

**Grounded verbatim (asos-tyrion-11.md):**

> "What did you do with her, after my little lesson?" … "I suppose the steward sent her
> on her way. I never thought to inquire." "On her way where?" "Wherever whores go."
> — `asos-tyrion-11.md:253–257`

> "Wherever whores go" is the line that fires the crossbow AND establishes the obsession
> Tyrion carries into ADWD.

**Tier:** Tier 1 (on-page cause of the seeking behavior confirmed in ADWD chapters)
**Rationale:** This is the highest-value cross-arc seam this lens can find — it wires the
Tywin-death arc forward into the Essos arc. The revelation event should have an outgoing
CAUSES edge to `tyrion-lannister SEEKS tysha`, or at minimum the MOTIVATES tyrion edge
already present should carry this interpretation. Since `MOTIVATES` is reserved for
CHARACTER targets, and `tyrion-lannister SEEKS tysha` is a dyadic edge (not an event
node), the right read is that the event MOTIVATES tyrion-lannister AND the SEEKS edge
already captures the downstream behavior — the seam is soft-complete. Still, the explicit
CAUSES link from `jaime-reveals-the-truth-of-tysha` to the SEEKS edge is worth noting as
already structurally encoded via the MOTIVATES tyrion route.

**Verdict:** The structural chain exists (MOTIVATES tyrion → SEEKS tysha). No new edge
needed beyond confirming the chain is traversable. **Soft-complete; note for orchestrator.**

---

### SEAM 8 — assassination-of-tywin-lannister CAUSES tommen-baratheon (accession as king) — does a node exist?

**Check:** Is there a `tommen-ascends-as-king` or `coronation-of-tommen` event node?
Searching graph nodes: no such event node found (only `wedding-of-tommen-i-baratheon-and-margaery-tyrell`).
The existing `assassination-of-tywin-lannister CAUSES cersei-rearms-the-faith-and-forgives-the-debt`
is the only forward-wired consequence. Tommen's accession as king is the necessary
intermediate but the node does not exist. **Node missing — see prose note below.**

---

### SEAM 9 — murder-of-elia-martell-and-rhaegars-children MOTIVATES gregor-confesses-and-kills-oberyn (backward causation — Oberyn's pursuit of Gregor IS caused by the murder)

**SOURCE:** `murder-of-elia-martell-and-rhaegars-children`
**EDGE:** `CAUSES`
**TARGET:** `gregor-confesses-and-kills-oberyn`

**Node check:**
- `murder-of-elia-martell-and-rhaegars-children` — EXISTS (event.assassination)
- `gregor-confesses-and-kills-oberyn` — EXISTS (event.death)

**Existing graph state:** No CAUSES or MOTIVATES edge from the murder to the combat event.
`gregor-confesses-and-kills-oberyn` has `oberyn-martell VICTIM_IN` and `cersei-lannister
COMMANDS_IN` and `trial-of-tyrion-lannister TRIGGERS` — but NO upstream link to the
murder that is Oberyn's reason for pursuing Gregor.

**Agency-check:** This is NOT an agency-collapse. CAUSES here does not erase Tyrion's
trial-demand or Cersei's deployment of Gregor. Rather, the murder is the structural
background condition that makes Oberyn WILLING to champion Tyrion and ABLE to get close
to Gregor. Without the murder, Oberyn has no motivation to enter the combat.

**However:** The right type is not CAUSES but MOTIVATES, with oberyn-martell as target,
which is SEAM 1 above. The murder does not directly CAUSE the combat event; it MOTIVATES
the person who drives the combat. The clean dyadic is SEAM 1. Proposing SEAM 1 is
sufficient; a direct murder→combat edge would over-attribute causation and bypass the
human agent (Oberyn).

**Verdict:** Covered by SEAM 1. **Do not add a separate murder→combat CAUSES edge** — that
collapses agency through Oberyn.

---

### SEAM 10 — tywin-lannister MANIPULATES jaime-lannister (Tysha lie — parallel to DECEIVES tyrion)

**SOURCE:** `tywin-lannister`
**EDGE:** `MANIPULATES`
**TARGET:** `jaime-lannister`

**Node check:**
- `tywin-lannister` — EXISTS
- `jaime-lannister` — EXISTS

**Grounded in text (asos-tyrion-11.md):**

> "She was no whore. I never bought her for you. That was a lie that Father commanded me
> to tell. … he said that you required a sharp lesson. That you would learn from it, and
> thank me later …"
> — `asos-tyrion-11.md:79–83`

Tywin commanded Jaime to lie, using paternal authority and a rationalized framing ("a
sharp lesson") to make Jaime complicit in the deception. Jaime was manipulated into
transmitting the lie that destroyed Tyrion's marriage.

**Existing graph state:** `tywin-lannister ASSAULTS jaime-lannister` exists (ASOS-Jaime-07
ref). No MANIPULATES edge from Tywin to Jaime via the Tysha command.

**Tier:** Tier 1
**Rationale:** This is a clean cross-arc dyadic character seam: Tywin manipulates Jaime
into complicity in the Tysha deception. The manipulation is what eventually creates the
guilt that drives Jaime to confess the truth to Tyrion in asos-tyrion-11, which in turn
CAUSES the assassination. It wires the Tysha deception character-to-character upstream of
the reveal. Tywin → Jaime → Tyrion is the causal chain; this edge names the first link.

---

### SEAM 11 — jaime-reveals-the-truth-of-tysha CAUSES OPPOSES / rupture between jaime-lannister and tyrion-lannister

**Check:** Is there an edge `tyrion-lannister OPPOSES jaime-lannister` or similar?
Searching the graph: no such edge exists. The revelation ends with Tyrion slapping Jaime
and threatening to pay him back, then saying "I killed your vile son" and walking away.
This is a relational rupture but the text is ambiguous: is it permanent, or just the heat
of the moment? Tyrion wants to call back; the rupture is emotional not structural. Given
that OPPOSES implies ongoing structural opposition (as with the many `jaime OPPOSES
cersei` type edges), and the text presents this as a grief-rage moment, not a permanent
faction break, this should NOT become an OPPOSES edge. **Rejected** — see Self-Rejected.

---

## SEAMS NEEDING A NEW NODE (prose notes for orchestrator)

**Tyrion-flees-to-Essos / Varys-smuggles-Tyrion event:** The chapter depicts a
substantial discrete event — Varys guides Tyrion through the secret tunnels, fourth-level
dungeons, sewers, and to a waiting galley. The text is explicit:

> "You're going down into the sewers, and from there to the river. A galley is waiting
> in the bay."
> — `asos-tyrion-11.md:57`

This is a named sequence with specific agents (Varys, Tyrion), a mechanism (secret
passages), a destination (Free Cities), and causal consequences (Tyrion arrives in Essos,
meets Illyrio). Currently no event node exists for this (the baseline confirmed it as a
mint candidate). Without it, the seam from `assassination-of-tywin-lannister` to Tyrion's
ADWD arc is broken. Recommended node type: `event.escape`, slug e.g.
`varys-smuggles-tyrion-from-kings-landing`. Agents: `varys AGENT_IN`, `tyrion-lannister
AGENT_IN`. CAUSES: some ADWD Tyrion-in-Essos event. ENABLES: the Essos arc broadly.

**Tommen's accession as king:** No coronation-of-tommen node exists. Tywin's death removes
the acting Hand and clears the way for Cersei's regency under Tommen. This event is the
structural intermediate between `assassination-of-tywin-lannister` and `cersei-rearms-the-faith`.
Consider minting a `tommen-ascends-the-iron-throne` event node when the Cersei-arc track
runs enrichment dips.

**Crossbow as artifact:** The crossbow Tyrion uses is taken from Tywin's wall (Tywin's
weapon, used to kill him). This object is potentially load-bearing (Tywin killed by his own
crossbow — there is poetic/thematic weight) but is not yet in the graph. A modest artifact
node `crossbow-of-tywin-lannister` could carry `KILLED_WITH` (Tywin KILLED_WITH crossbow)
and `WIELDED_IN` (assassination) edges. Low priority unless artifact tracking is being
expanded.

**Varys-Illyrio conspiracy as upstream cause:** `varys CONSPIRES_WITH illyrio-mopatis`
already exists. Whether the smuggling of Tyrion to Illyrio's manse is a *downstream
manifestation* of that conspiracy is answerable from ADWD but belongs to a different lens.
Note for the Tyrion-in-Essos arc when it runs.

---

## SELF-REJECTED (seams checked and refuted with reason)

**1. `jaime-lannister BREAKS_VOW jaime-frees-tyrion-from-the-black-cells`**
Checked in text. Jaime frames the act as "a debt I owed you" (asos-tyrion-11.md:63), not
as an oath violation. He is not acting against any explicit Kingsguard duty (Tyrion is a
prisoner of Tywin the Hand, not of the king's person), and the chapter contains no
invocation of vow, oath, or sworn duty. BREAKS_VOW would be inferential, not textual.

**2. `tyrion-lannister OPPOSES jaime-lannister` (post-revelation rupture)**
The slap + threatening words are a heat-of-grief moment. Tyrion considers calling back.
The text does not warrant a structural opposition edge; the brothers have no opposing
factions, agendas, or institutional positions post-chapter. OPPOSES would over-read the
emotional beat.

**3. `murder-of-elia-martell-and-rhaegars-children CAUSES gregor-confesses-and-kills-oberyn`**
This collapses Oberyn's human agency. The right path is SEAM 1: the murder MOTIVATES
Oberyn, and Oberyn's decision drives the combat. A direct event→event CAUSES edge bypasses
the human agent who is the actual driver.

**4. `cersei-lannister CAUSES assassination-of-tywin-lannister`**
Cersei triggered the trial and deployed Gregor, but she did not cause Tyrion to go up the
ladder to Tywin's chambers. Jaime's revelation (the actual upstream CAUSES) belongs to
Jaime, not Cersei. Cersei's role is COMMANDS_IN the trial and COMMANDS_IN the Gregor
deployment — she is not causally proximate to the assassination itself.

**5. `assassination-of-tywin-lannister CAUSES jaime-lannister (arc consequence)`**
Checking whether Tywin's death causally wires to any specific Jaime-arc node — Jaime burns
Cersei's letter after Tywin dies, representing his emotional break. But there is no event
node for `jaime-burns-cersei-letter` in the graph. Without a target node, no edge can be
proposed. Note for orchestrator: a Jaime-arc enrichment dip should look for this.

**6. `gregor-confesses-and-kills-oberyn MOTIVATES cersei-lannister` (counter-productive: Cersei's rearms follows Tywin's death, not Oberyn's death directly)**
The causal path from Oberyn's death to `cersei-rearms` goes through
`jaime-frees-tyrion → assassination-of-tywin → cersei-rearms`. Cersei rearming the Faith
is motivated by her NEED for power without Tywin — not by Oberyn's death as such. The
existing `assassination-of-tywin-lannister CAUSES cersei-rearms` edge correctly handles
this. No new edge needed.

---

## HARVEST

Notable finds encountered while reading the four chapters — point-captures for future
harvest passes. Do not extract; a harvest pass will attach.

| ref | kind | note |
|-----|------|------|
| `asos-tyrion-08.md:133` | FOOD | First wedding-feast course: creamy mushroom and buttered snail soup in gilded bowls; Tyrion eats quickly, Sansa takes one spoonful and pushes bowl away |
| `asos-tyrion-08.md:145` | FOOD | Second course: pastry coffyn filled with pork, pine nuts, and eggs |
| `asos-tyrion-08.md:153` | FOOD | sweetcorn fritters, hot oatbread with dates/apple/orange, wild boar rib — Tyrion eating during Hamish's songs |
| `asos-tyrion-08.md:155` | FOOD | trout in crushed almond crust; roast herons; cheese-and-onion pies; crabs in fiery eastern spices; chopped mutton in almond milk with carrots/raisins/onions; fish tarts |
| `asos-tyrion-08.md:157` | FOOD | honey-ginger partridge (Tyrion double helping); peacocks roasted whole stuffed with dates, served in plumage |
| `asos-tyrion-08.md:171` | FOOD | blandissory: beef broth + boiled wine, sweetened with honey, almonds, capon chunks; buttered pease; slivers of swan in saffron-peach sauce |
| `asos-tyrion-08.md:171` | FOOD | skewers of blood sausage "brought sizzling to the tables" — paired with a juggler for dark comic effect |
| `asos-tyrion-08.md:203` | FOOD | roundels of elk stuffed with ripe blue cheese |
| `asos-tyrion-08.md:205` | FOOD | leche of brawn spiced with cinnamon, cloves, sugar, almond milk — Tyrion toying with it when Joffrey lurches up |
| `asos-tyrion-08.md:289` | FOOD | pigeon pie — Joffrey jams his hand in Tyrion's slice, eats it, and chokes; the pie is the murder vehicle |
| `asos-tyrion-08.md:141` | HOSPITALITY/DESCRIPTION | tender husband feeding wife morsels from his plate + hand on her belly (Fossoway couple) — Tyrion watches enviously; first-class hospitality/intimacy observation |
| `asos-tyrion-08.md:99` | DESCRIPTION | Sansa performs courtly duties beautifully (complimenting Lancel, Elinor Tyrell, asking Jalabhar Xho about Summer Isles wedding customs) — Tyrion notes she would have made Joffrey a good queen |
| `asos-tyrion-09.md:245–247` | OBJECT | Grand Maester Pycelle lays out poison jars at trial: greycap (toadstool), nightshade, sweetsleep, demon's dance, blindeye, widow's blood, wolfsbane, basilisk venom, tears of Lys; also names "the strangler" as what killed Joffrey |
| `asos-tyrion-10.md:57` | FOOD | Tyrion's last decent meal before the combat: fried bread, blood sausage, applecakes, double eggs with onions and fiery Dornish peppers |
| `asos-tyrion-10.md:101` | FOOD | Tyrion's prison food morning of execution day: fried bread, blood sausage, applecakes, double eggs with onions and fiery Dornish peppers — same meal; he vomits it after Oberyn is killed (247) |
| `asos-tyrion-10.md:167` | DESCRIPTION | Full description of Gregor's armor: heavy plate over chainmail, dull grey steel dinted/scarred, boiled leather + quilting underneath, flat-topped greathelm bolted to gorget, stone fist crest; shield painted over with seven-pointed star (Andal symbol, Cersei's pious gesture) |
| `asos-tyrion-10.md:173` | DESCRIPTION | Oberyn's light armor: greaves, vambraces, gorget, spaulder, steel codpiece; copper scales over byrnie; half-helm with no visor; polished round shield showing sun-and-spear in four golds + copper |
| `asos-tyrion-10.md:123` | OBJECT | Oberyn's spear description: turned ash eight feet long, last two feet steel leaf-shaped spearhead; shaft oiled (possibly poisoned — manticore venom implied) |
| `asos-tyrion-11.md:197` | OBJECT | Shae wearing the Hand's chain of linked golden hands about her throat when Tyrion finds her in Tywin's bed — she is strangled with it; load-bearing artifact (the chain) |
| `asos-tyrion-09.md:135–159` | DESCRIPTION | Oberyn's extended pre-battle story of the Casterly Rock visit: mothers arranged marriages (Elia for Jaime, Cersei for Oberyn); Tywin rejected Elia as bride for Jaime and "offered you instead" (Tyrion) — Oberyn's mother took it as an outrage; full provenance of the Dorne-Lannister enmity |
| `asos-tyrion-08.md:19–25` | FORESHADOWING | Tyrion's interior monologue concluding Joffrey ordered the Bran assassination: "The prince's own dagger had a jeweled pommel … Instead he went poking among his father's weapons" — direct confirmation of the Littlefinger's-dagger plotline; load-bearing foreshadowing callback |
| `asos-tyrion-09.md:379` | FORESHADOWING | Oberyn to Tyrion: "Your father may not live forever" — said obliquely about Doran's Myrcella succession ambitions; on-page Chekhov pointing to Tywin's death this same night |
