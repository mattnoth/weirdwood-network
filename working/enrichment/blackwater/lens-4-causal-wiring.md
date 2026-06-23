# Blackwater enrichment — Lens 4: Existing-node ↔ existing-node causal wiring

> Produced: 2026-06-23
> Lens: Cross-arc seam (node↔node, PROPOSE ONLY — no minting)
> Dedup baseline: `working/enrichment/blackwater/baseline.md` read in full.

---

## PROPOSED EDGES

---

### EDGE L4-01

**`battle-of-oxcross` --ENABLES--> `battle-of-the-blackwater`**

| Field | Value |
|---|---|
| Tier | 2 |
| Type | ENABLES |
| Chapter:line | `sources/chapters/acok/acok-tyrion-13.md:21` |
| Container note | CROSS-CONTAINER: battle-of-oxcross (wo5k/north) → battle-of-the-blackwater (wo5k) |

**Verbatim quote (grounding):**
> "He'd never had his brother Robert's thirst for battle. He would command from the rear, from the reserve, much as Lord Tywin Lannister was wont to do."

**Secondary grounding — `battle-of-the-fords` node body (already confirmed in graph):**
> "Expecting Stannis Baratheon to be preoccupied for months with the siege of Storm's End, Lord Tywin Lannister risks leaving Harrenhal to stop Robb's raiding of his homeland."

**Rationale:** Robb's victory at Oxcross is the proximate cause of Tywin marching west out of Harrenhal. Tywin's departure westward is exactly what opened the strategic window for Stannis to besiege King's Landing. Without Oxcross drawing Tywin away, Stannis cannot rationally gamble on a river assault against a full Lannister garrison. This is ENABLES (not CAUSES): Oxcross creates the precondition (Tywin absent, KL vulnerable), but Stannis's own decision and forces are the proximate agent of the assault. No temporal inversion: Oxcross is ACOK ch. 33, the Blackwater is ACOK ch. 59–62. Not sibling-beats — these are separate events in different theaters. Agency check: passes (a third party, Stannis, makes the free choice to attack).

**Both endpoints exist:** `battle-of-oxcross` ✓ (confirmed node read), `battle-of-the-blackwater` ✓ (hub node).

---

### EDGE L4-02

**`battle-of-the-fords` --ENABLES--> `battle-of-the-blackwater`**

| Field | Value |
|---|---|
| Tier | 2 |
| Type | ENABLES |
| Chapter:line | `graph/nodes/events/battle-of-the-fords.node.md` (## Aftermath) — wiki-sourced, Tier-3 provenance for the specific causal chain but mechanically established |

**Verbatim quote (from `battle-of-the-fords` node ## Aftermath, wiki-sourced):**
> "Edmure's defense of the fords delayed Tywin long enough for riders from Bitterbridge to inform him of happenings in the east, however. With Lord Petyr Baelish having negotiated an alliance between House Tyrell and House Baratheon of King's Landing, Tywin turned back east, rendezvousing with Lords Mace Tyrell, Mathis Rowan, and Randyll Tarly. The combined army then defeated Stannis in the Battle of the Blackwater."

**Rationale:** The Battle of the Fords is the bottleneck event that stopped Tywin from reaching the westerlands and forced him to hold at the Red Fork — the delay created the window for Littlefinger's Tyrell-Lannister deal to reach Tywin while he was still near the center of the continent, allowing him to pivot east in time to arrive at the Blackwater. The battle-of-the-fords ENABLES the Blackwater (Tywin's timely relief march); it does not CAUSE it (the battle's outcome does not mechanically produce the Blackwater — Tywin's voluntary pivot is the proximate agent). Not already in the spine (baseline lists only battle-of-oxcross and littlefinger-brokers as upstream ENABLES; battle-of-the-fords is a distinct node and a distinct causal link). Temporal: the Fords (ACOK ch. 46) precede the Blackwater (ACOK ch. 59–62). Both endpoints confirmed as existing nodes.

**Both endpoints exist:** `battle-of-the-fords` ✓ (confirmed node read, ## Aftermath explicitly names the Blackwater as downstream), `battle-of-the-blackwater` ✓.

---

### EDGE L4-03

**`battle-of-the-blackwater` --CAUSES--> `tyrion-processes-the-assassination-attempt`**

| Field | Value |
|---|---|
| Tier | 2 |
| Type | CAUSES |
| Chapter:line | `sources/chapters/acok/acok-tyrion-15.md:97` |

**Verbatim quote:**
> "He remembered now. The bridge of boats, Ser Mandon Moore, a hand, a sword coming at his face. If I had not pulled back, that cut would have taken off the top of my head. Jaime had always said that Ser Mandon was the most dangerous of the Kingsguard, because his dead empty eyes gave no hint to his intentions. I should never have trusted any of them. He'd known that Ser Meryn and Ser Boros were his sister's, and Ser Osmund later, but he had let himself believe that the others were not wholly lost to honor. Cersei must have paid him to see that I never came back from the battle. Why else?"

**Rationale:** The assassination attempt by Ser Mandon Moore occurs during the battle (ACOK Tyrion XIV) and produces the downstream event `tyrion-processes-the-assassination-attempt` (ACOK Tyrion XV) as a direct causal consequence — the battle is what created the context in which Cersei could plausibly arrange Tyrion's death (chaos of combat, deniability, the cover of the fire and the bridge of ships). The processing event exists only because the attempt happened during the battle. CAUSES is correct: the battle (mediated by Cersei's arrangement) produces the assassination attempt which produces Tyrion's near-death, disfigurement, and reckoning. Not temporal inversion: Tyrion XV is post-battle. Not sibling/constitutive: the processing event is a downstream mental and physical reckoning, not a constitutive piece of the battle itself. Agency: Cersei's arrangement mediates, but the chain is tight enough for CAUSES (the battle provides the unique cover).

**Both endpoints exist:** `battle-of-the-blackwater` ✓, `tyrion-processes-the-assassination-attempt` ✓ (confirmed node read, evidence_chapters: ACOK Tyrion XV, minted-plate3 stub).

---

### EDGE L4-04

**`battle-of-the-blackwater` --CAUSES--> `tywin-named-savior-of-the-city`** *(already in spine — SKIP; see below)*

*Confirmed in baseline. Do not re-propose.*

---

### EDGE L4-05

**`tywin-named-savior-of-the-city` --CAUSES--> `tyrion-processes-the-assassination-attempt`**

| Field | Value |
|---|---|
| Tier | 2 |
| Type | CAUSES |
| Chapter:line | `sources/chapters/acok/acok-tyrion-15.md:107` |

**Verbatim quote:**
> "Your own . . . my lord, that would not be possible. The King's Hand has taken up residence in your former chambers."
> "I. Am. King's Hand."
> Maester Ballabar looked distressed. "No, my lord, I . . . you were wounded, near death. Your lord father has taken up those duties now. Lord Tywin, he . . ."

**Rationale:** Tywin's arrival and immediate assumption of the Handship is what completes the double blow to Tyrion: physically disfigured and politically displaced simultaneously. The processing event node (ACOK Tyrion XV) encompasses both Tyrion's reckoning with Mandon Moore's treachery AND his discovery of political displacement. `tywin-named-savior-of-the-city` is the upstream event node that precipitates the political content of Tyrion XV. CAUSES is appropriate: Tywin's elevation directly and immediately produces the situation that Tyrion processes (he is displaced while bedridden). Temporal: Tywin's arrival is the battle night (per Maester Ballabar "since the night of the battle"), Tyrion XV is a day or days later — no inversion. Not constitutive (different events, different chapters).

**Both endpoints exist:** `tywin-named-savior-of-the-city` ✓ (confirmed in baseline + causal chain output), `tyrion-processes-the-assassination-attempt` ✓.

---

### EDGE L4-06

**`battle-of-the-blackwater` --TRIGGERS--> `sandor-clegane`** *(character target — wrong type)*

*Rejected.* MOTIVATES requires character target, but we cannot use MOTIVATES on a character for "Sandor deserts" because there is no event node for that desertion yet, and MOTIVATES target must be a character actor not a character entity node. See DEPENDENCIES below — this wiring is contingent on an event node being minted for Sandor's desertion.

---

### EDGE L4-07

**`joffrey-sets-sansa-aside-and-agrees-to-wed-margaery` --ENABLES--> `purple-wedding`**

| Field | Value |
|---|---|
| Tier | 2 |
| Type | ENABLES |
| Chapter:line | `sources/chapters/acok/acok-sansa-08.md:41` (quote already on `joffrey-sets-sansa-aside` node body) |
| Container note | CROSS-CONTAINER: the sansa-aside event (wo5k/ACOK) opens the door to the Purple Wedding (wo5k/ASOS) |

**Verbatim quote (on the `joffrey-sets-sansa-aside` node ## Quotes, grounded to ACOK Sansa VIII:41):**
> "Your Grace, in the judgment of your small council, it would be neither proper nor wise for you to wed the daughter of a man beheaded for treason, a girl whose brother is in open rebellion against the throne even now. Sire, your councillors beg you, for the good of your realm, set Sansa Stark aside. The Lady Margaery will make you a far more suitable queen."

**Rationale:** The formal setting-aside of Sansa (ACOK Sansa VIII) is the event that constitutes the betrothal of Joffrey to Margaery. This is the direct, necessary precondition for the Purple Wedding (ASOS) — without this event there is no Joffrey-Margaery marriage. ENABLES is correct: joffrey-sets-sansa-aside opens the formal gate (the setting-aside + betrothal), but the purple-wedding occurs only after multiple planning/preparation steps (Tywin sets the date, the hairnet is obtained, etc.) — a third-party chain intervenes, so ENABLES not CAUSES. Temporal: ACOK Sansa VIII precedes ASOS by the entire in-universe gap. Not sibling beats. Cross-container seam: both nodes in wo5k container, but this links two distinct arcs — ACOK political aftermath → ASOS murder plot arc.

**Both endpoints exist:** `joffrey-sets-sansa-aside-and-agrees-to-wed-margaery` ✓ (confirmed node read, minted-plate3), `purple-wedding` ✓ (confirmed node read, full wiki-promotion).

---

### EDGE L4-08

**`battle-of-the-blackwater` --ENABLES--> `purple-wedding`**

| Field | Value |
|---|---|
| Tier | 2 |
| Type | ENABLES |
| Chapter:line | `sources/chapters/acok/acok-sansa-07.md:145` |
| Container note | CROSS-CONTAINER: wo5k Blackwater arc → wo5k Purple Wedding arc (cross-spine seam) |

**Verbatim quote:**
> "It was Lord Renly! Lord Renly in his green armor, with the fires shimmering off his golden antlers! Lord Renly with his tall spear in his hand! They say he killed Ser Guyard Morrigen himself in single combat, and a dozen other great knights as well. It was Renly, it was Renly, it was Renly! Oh! the banners, darling Sansa! Oh! to be a knight!"

**Supplementary grounding — `purple-wedding` node body (## Origins):**
> "After the Battle of the Blackwater, Joffrey discards Sansa Stark and is betrothed to Margaery."

**Rationale:** The battle's victory ENABLES the Purple Wedding by creating the political conditions under which the Tyrell-Lannister alliance is cemented (Tywin arrives as savior, the deal is sealed in blood on the Blackwater) and Joffrey can be safely set aside from Sansa and married to Margaery. Without the battle (and specifically the Tyrell role in the victory — Garlan-as-Renly's-ghost routing Stannis's men) the Tyrell alliance has no military proof-of-value and no basis for the wedding. ENABLES not CAUSES: the wedding requires many intermediate steps (betrothal, planning, the hairnet plot, etc.). Distinct from L4-07: this edge runs from the battle hub itself directly to the purple-wedding, capturing the strategic-level causal link; L4-07 runs from the specific betrothal event. Both are needed: one is the macro causal claim, one the direct mechanism.

**Dedup check:** Baseline lists `battle-of-the-blackwater CAUSES joffrey-sets-sansa-aside` — that downstream edge exists. This proposed edge (battle → purple-wedding) is a longer skip that is NOT in the baseline causal spine (baseline lists no direct blackwater → purple-wedding edge).

**Both endpoints exist:** `battle-of-the-blackwater` ✓, `purple-wedding` ✓.

---

### EDGE L4-09

**`stannis-absorbs-renly-s-host` --ENABLES--> `littlefinger-brokers-tyrell-lannister-alliance`**

*Already in baseline as ENABLES. Do not re-propose.*

---

### EDGE L4-10

**`garlan-tyrell` --MOTIVATES--> `stannis-retreats-to-dragonstone`**

| Field | Value |
|---|---|
| Tier | 2 |
| Type | TRIGGERS (not MOTIVATES — see rationale) |
| Chapter:line | `sources/chapters/acok/acok-sansa-07.md:145` |
| Container note | Cross-arc seam: Tyrell entry at Blackwater → Stannis retreat chain |

**Verbatim quote:**
> "Lord Renly in his green armor, with the fires shimmering off his golden antlers! Lord Renly with his tall spear in his hand! They say he killed Ser Guyard Morrigen himself in single combat, and a dozen other great knights as well. It was Renly, it was Renly, it was Renly!"

**Corrected type: TRIGGERS.** Garlan wearing Renly's armor and leading the vanguard into Stannis's host is the immediate psychological and military spark that breaks Stannis's bannermen (they shout for "Lord Renly!" and go over or flee), directly producing the rout that forces Stannis's retreat. No significant mediation: the rout is the retreat. TRIGGERS is the right type — immediate next-event production. MOTIVATES would require the target to be a character, and `stannis-retreats-to-dragonstone` is an event node. Temporal: Garlan's charge (ACOK Sansa VII during battle night) → retreat (same night/aftermath). Not co-location: the causal mechanism is explicit in the text.

**Proposed edge:** `garlan-tyrell` --TRIGGERS--> `stannis-retreats-to-dragonstone`

**Both endpoints exist:** `garlan-tyrell` ✓ (confirmed node; aliases include "Lord Renly's shade"), `stannis-retreats-to-dragonstone` ✓ (confirmed node read).

---

### EDGE L4-11

**`imry-florent` --CAUSES--> `battle-of-the-blackwater`** *(wrong direction — reject)*

*Imry's command error (rowing past the chain, not probing cautiously) contributed to the catastrophe, but `imry-florent` is a character node and cannot CAUSE an event node. The appropriate framing is role edges (COMMANDS_IN, VICTIM_IN). Defer to Lens 2 (participants). Not a cross-arc seam.*

---

### EDGE L4-12

**`the-antler-men-conspiracy` --ENABLES--> `battle-of-the-blackwater`**

| Field | Value |
|---|---|
| Tier | 2 |
| Type | ENABLES |
| Chapter:line | `sources/chapters/acok/acok-tyrion-13.md:41` |

**Verbatim quote:**
> "Joff had the Antler Men trussed up naked in the square below, antlers nailed to their heads. When they'd been brought before the Iron Throne for justice, he had promised to send them to Stannis. A man was not as heavy as a boulder or a cask of burning pitch, and could be thrown a deal farther."

**Rationale:** The Antler Men conspiracy's suppression enables the battle by eliminating a potential fifth-column inside the city (pro-Stannis nobles who might open gates or signal positions during the siege). With them captured and displayed as catapult ammunition, Tyrion neutralizes an internal threat that could have unraveled the defense. ENABLES (precondition): Tyrion's preparations (the wildfire, the chain, the Antler Men suppression) together enable the battle outcome; no single one causes the battle. Temporal: Antler Men exposed ACOK Tyrion XII (ch. 48), battle ACOK ch. 59–62. Not sibling. The Antler Men node exists as a bare stub (confirmed node read); this edge wires it into the causal graph for the first time.

**Both endpoints exist:** `the-antler-men-conspiracy` ✓ (confirmed node read, minted-plate3), `battle-of-the-blackwater` ✓.

---

### EDGE L4-13

**`battle-of-the-blackwater` --CAUSES--> `kingsguard-investiture-ceremony`**

> **Flag — uncertain target.** The `kingsguard-investiture-ceremony` node (confirmed read: minted-plate3, evidence_chapters ACOK Tyrion XI) is set BEFORE the battle (ch. 55, Tyrion XI). That is the ceremony where Ser Mandon Moore was already a Kingsguard member. The post-battle investiture of Loras Tyrell (replacing Mandon Moore, who drowned) occurs in ASOS, not in ACOK. There is NO node for "Loras joins the Kingsguard" in the events directory (checked). This edge cannot be proposed without that node existing. See DEPENDENCIES.

---

## EDGE SUMMARY TABLE

| ID | Edge | Type | Chapter:line | Cross-container? |
|---|---|---|---|---|
| L4-01 | `battle-of-oxcross` → `battle-of-the-blackwater` | ENABLES | acok-tyrion-13.md:21 | same container (wo5k) |
| L4-02 | `battle-of-the-fords` → `battle-of-the-blackwater` | ENABLES | battle-of-the-fords node ## Aftermath (wiki-cite) | same container |
| L4-03 | `battle-of-the-blackwater` → `tyrion-processes-the-assassination-attempt` | CAUSES | acok-tyrion-15.md:97 | same container |
| L4-05 | `tywin-named-savior-of-the-city` → `tyrion-processes-the-assassination-attempt` | CAUSES | acok-tyrion-15.md:107 | same container |
| L4-07 | `joffrey-sets-sansa-aside-and-agrees-to-wed-margaery` → `purple-wedding` | ENABLES | acok-sansa-08.md:41 | same container (wo5k), cross-arc spine |
| L4-08 | `battle-of-the-blackwater` → `purple-wedding` | ENABLES | acok-sansa-07.md:145 | same container, cross-spine seam |
| L4-10 | `garlan-tyrell` → `stannis-retreats-to-dragonstone` | TRIGGERS | acok-sansa-07.md:145 | same container |
| L4-12 | `the-antler-men-conspiracy` → `battle-of-the-blackwater` | ENABLES | acok-tyrion-13.md:41 | same container |

---

## DEPENDENCIES

Edges that require a node another lens is likely minting — cannot be proposed until those nodes exist:

1. **Sandor deserts during the Blackwater** — Sandor's departure from the Kingsguard / King's Landing is a richly textured event (the confrontation with Tyrion, the drunken visit to Sansa's chamber, the white cloak left behind). No event node exists for it. With that node, the following edges become proposable:
   - `battle-of-the-blackwater` --TRIGGERS--> `sandor-deserts-kingsguard` (the battle's fires are the direct psychological trigger; "I've lost half my men. I'm not taking more into that fire")
   - `sandor-deserts-kingsguard` --ENABLES--> (later: Sandor's arc as the Hound traveling the Riverlands with Arya)
   Recommend Lens 2 or a dedicated event lens mint this node with slug `sandor-deserts-during-the-blackwater`.

2. **Loras Tyrell joins the Kingsguard** — No event node exists for Loras's investiture (which happens post-Blackwater, replacing Mandon Moore). With that node:
   - `battle-of-the-blackwater` --ENABLES--> `loras-tyrell-joins-kingsguard` (Mandon Moore drowned, vacancy opened)
   This would create the cross-arc seam from Blackwater to the Kingsguard arc and Loras's eventual fate at Dragonstone.

3. **Tyrion sidelined / displaced as Hand** — `tyrion-processes-the-assassination-attempt` covers this in part, but a cleaner "Tyrion displaced as Hand of the King" event node (if minted) would enable:
   - `tywin-named-savior-of-the-city` --CAUSES--> `tyrion-displaced-as-hand`
   - `battle-of-the-blackwater` --CAUSES--> `tyrion-displaced-as-hand`
   Currently using `tyrion-processes-the-assassination-attempt` as the downstream target, which captures this indirectly.

---

## HARVEST

While grounding these edges, the following notable passages were encountered and are flagged for a later harvest pass:

- `acok-tyrion-13.md:11` / **description** / Tyrion atop the merlon watching the wildfire: "The low clouds caught the color of the burning river and roofed the sky in shades of shifting green, eerily beautiful. A terrible beauty. Like dragonfire. Tyrion wondered if Aegon the Conqueror had felt like this as he flew above his Field of Fire." — dragonfire comparison / foreshadowing candidate (Field of Fire parallel)

- `acok-tyrion-13.md:31` / **description** / "Hallyne said that sometimes the substance burned so hot that flesh melted like tallow." — grim physical description, wildfire properties

- `acok-tyrion-14.md:39` / **character description** / Battle fever passage — Tyrion on the bridge of boats: "How time seemed to blur and slow and even stop…You stop feeling, you stop thinking, you stop being you, there is only the fight, the foe…" — character interiority, Jaime's voice echoed in Tyrion's head (cross-POV)

- `acok-davos-03.md:105-107` / **description** / The wildfire ignition from Davos's POV: "With a grinding, splintering, tearing crash, Swordfish split the rotted hulk asunder…From inside her Davos saw green gushing from a thousand broken jars, poison from the entrails of a dying beast, glistening, shining, spreading across the surface of the river." — vivid grim food-adjacent register ("poison from the entrails"; no actual food, but the visceral body-horror of the killing fluid)

- `acok-davos-03.md:137` / **description** / "Black Betha burning, and White Hart and Loyal Man to either side. Piety, Cat, Courageous, Sceptre, Red Raven, Harridan, Faithful, Fury, they had all gone up, Kingslander and Godsgrace as well, the demon was eating his own." — ship-naming catalog; also: the wildfire "demon" imagery echoes later ADWD dragon metaphors

- `acok-sansa-07.md:59` / **description** / Sansa watching the battle from her window: "The southern sky was aswirl with glowing, shifting colors, the reflections of the great fires that burned below. Baleful green tides moved against the bellies of the clouds, and pools of orange light spread out across the heavens." — rich visual description, worth attaching as Sansa's witness imagery

- `acok-tyrion-15.md:13` / **description** / Tyrion's post-battle dream: "The sun was a hot white penny, shining down upon the grey river as it rushed around the charred bones of sunken ships… My work, thought Tyrion Lannister. They died at my command." — guilt/character depth; foreshadows themes of moral weight of command

---

## NOTES

1. **L4-01 vs. L4-02 both warranted:** The battle-of-the-fords and battle-of-oxcross play *distinct* ENABLES roles: Oxcross draws Tywin out; the Fords trap him long enough for the Tyrell deal to arrive. Both are real causal links; neither subsumes the other.

2. **L4-07 + L4-08 are complementary, not redundant:** L4-07 links the specific betrothal event to the wedding; L4-08 links the overall battle to the wedding as a strategic precondition. Both are needed for graph traversal (different query paths will find one or the other depending on starting node).

3. **`wildfire-plot` dedup confirmed:** I never proposed any edge to `wildfire-plot` (the Aerys II node). All Blackwater wildfire references treated as a new, to-be-minted node (`wildfire-trap-on-the-blackwater`) per baseline instructions. No such node was proposed in this lens — that is Lens 2/3 territory.

4. **`garlan-tyrell` → `stannis-retreats` (L4-10):** Garlan's aliases include "Lord Renly's shade" (confirmed on node frontmatter). The causal mechanism is the psychological rout of Stannis's bannermen who mistake him for Renly's ghost. This is a clean, book-grounded TRIGGERS edge and one of the highest-value seams in this lens — it wires a character node directly into the causal arc that eventually leads to the Wall.

5. **Cross-container seams found:** The most consequential cross-arc seam in this lens is L4-08 (`battle-of-the-blackwater` → `purple-wedding`), which bridges the ACOK battle arc to the ASOS murder-conspiracy arc within the wo5k container. Secondary: L4-10 (`garlan-tyrell` → `stannis-retreats`) is the proximate wiring that links the Tyrell entry to the NORTH spine chain (stannis-retreats → stannis-moves-to-wall → battle-beneath-the-wall → …).
