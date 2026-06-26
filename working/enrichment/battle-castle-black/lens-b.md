# Lens B — whodunit / revelation / hidden-agency — proposals

> Battle of Castle Black enrichment dip · Lens B (whodunit/revelation/hidden-agency)
> Source chapters: asos-jon-05 through asos-jon-11
> Dedup baseline: internal-edges.txt (180 edges) + baseline.md gap analysis

---

## PROPOSED NODES

1. **slug:** `ygritte-shot-at-castle-black`
   **name:** Death of Ygritte at Castle Black
   **type:** event.death
   **containers:** [north, jon]
   **description:** Ygritte is struck by an arrow (black shaft, white duck-feather fletching — not Jon's grey-goose arrows) during the southern Thenn assault on Castle Black. She dies in Jon's arms beneath the Lord Commander's Tower. The arrow's origin is unresolved by the text; Jon notes it is not one of his own but feels guilt nonetheless. Jon burns her body north of the Wall.
   **evidence_ref:** asos-jon-07.md:189–206

2. **slug:** `jon-assigned-to-kill-mance`
   **name:** Jon sent to assassinate Mance Rayder
   **type:** event.incident
   **containers:** [north, jon]
   **description:** Janos Slynt and Ser Alliser Thorne, unable to legally execute Jon, send him to Mance's camp under the pretense of "treating" but with secret orders to kill the King-beyond-the-Wall. Jon recognizes the trap: if he kills Mance, the wildlings kill him; if he refuses or fails, Slynt brands him a coward. Maester Aemon's protection of Jon (letter to Cotter Pyke) forced this alternative to the ice cell.
   **evidence_ref:** asos-jon-10.md:53–55

3. **slug:** `mance-conceals-horn-of-winter`
   **name:** Mance conceals discovery of Horn of Winter
   **type:** event.incident
   **containers:** [north, jon]
   **description:** Mance Rayder had found and possessed the Horn of Winter (Joramun's horn) before and during the assault on Castle Black, but told his people — including Ygritte, who passed the claim to Jon — that he had never found it. He chose not to use it despite possessing it, weighing sorcerous risk against his tactical position. Jon's discovery of the horn during the parley is the revelation beat.
   **evidence_ref:** asos-jon-10.md:159–165

---

## PROPOSED EDGES

### Thread 1: Jon as double-agent — deepening the DECEIVES / SPIES_ON layer

**E-B-01**
- `jon-snow` | DECEIVES | `styr` | tier=1
- qualifier: covert Watch loyalist posing as deserter in Styr's southern infiltration party
- evidence_ref: asos-jon-05.md:93
- quote: "After each day's march the Magnar summoned him to ask shrewd sharp questions about Castle Black, its garrison and defenses. Jon lied where he dared and feigned ignorance a few times"
- rationale: Jon actively lies to Styr during the march south — direct deception, not merely concealment. `jon-snow SERVES styr` exists (the pretence); this is the deliberate-deceit layer on top of it.
- status: NEW

**E-B-02**
- `jon-snow` | DECEIVES | `mance-rayder` | tier=1
- qualifier: pretended desertion from Watch throughout wildling infiltration period
- evidence_ref: asos-jon-10.md:165
- quote: "Did you think only crows could lie? I liked you well enough, for a bastard . . . but I never trusted you."
- rationale: Mance's own words confirm Jon's ongoing deception of him. `jon-snow SPIES_ON mance-rayder` already exists, but DECEIVES captures the active false-identity layer (presenting as a turncloak) distinct from intelligence-gathering. DEDUP check: `jon-snow SPIES_ON mance-rayder` [1] exists; `jon-snow DECEIVES mance-rayder` does NOT appear in internal-edges.txt.
- status: NEW

**E-B-03**
- `jon-snow` | REVEALS_TO | `donal-noye` | tier=1
- qualifier: reveals Styr's southern infiltration force and the wildling southern attack plan
- evidence_ref: asos-jon-06.md:59–63
- quote: "There are wildlings south of the Wall, coming up from Queenscrown to open the gate." / "A hundred and twenty, and well armed for wildlings."
- rationale: Jon's betrayal of the Thenns' plan to Noye is the pivotal intelligence disclosure that saves Castle Black. No REVEALS_TO edge for this exists; only `aemon-targaryen-son-of-maekar-i HEALS jon-snow` and `donal-noye PROTECTS jon-snow` are wired for this scene.
- status: NEW

**E-B-04**
- `jon-snow` | REVEALS_TO | `aemon-targaryen-son-of-maekar-i` | tier=1
- qualifier: discloses Styr's force, Mance's tactics, and his own spy mission (admitting oathbreaking)
- evidence_ref: asos-jon-06.md:127
- quote: "I was with them. Qhorin Halfhand commanded me to join them. . . . I broke my vows with her. I never meant to, but . . . I wasn't strong enough."
- rationale: This is a confession/revelation beat, not a healing interaction — Jon discloses his undercover status and oathbreaking to Aemon. `aemon-targaryen-son-of-maekar-i HEALS jon-snow` covers the medical scene; REVEALS_TO captures the intelligence/confession beat in the same scene. DEDUP check: no `jon-snow REVEALS_TO aemon-targaryen-son-of-maekar-i` in internal-edges.txt.
- status: NEW

**E-B-05**
- `jon-snow` | BREAKS_VOW | `nights-watch` | tier=1
- qualifier: Jon's explicit admission to Aemon and Noye of oathbreaking (sexual vow) during the spy mission
- evidence_ref: asos-jon-09.md:155
- quote: "I broke my vows with a woman. I admit that. Yes."
- rationale: Jon's explicit on-record admission before Janos Slynt's tribunal. DEDUP check: `jon-snow BREAKS_VOW stannis-baratheon` [1] (adwd-jon-08) exists — that is a different vow/event. No `jon-snow BREAKS_VOW nights-watch` exists in internal-edges.txt. This is the ASOS admission beat, not the ADWD one. Source should be `nights-watch` as institutional target of the vow.
- status: NEW (different target/event from existing adwd BREAKS_VOW edge)

### Thread 2: Mance's two-pronged deception and the Bowen Marsh bait

**E-B-06**
- `mance-rayder` | DECEIVES | `bowen-marsh` | tier=1
- qualifier: raiding-party feints along the Wall draw Marsh out, leaving Castle Black weakly defended
- evidence_ref: asos-jon-06.md:51
- quote: "Feints. Mance wants us to spread ourselves thin, don't you see? . . . And Bowen Marsh has obliged him."
- rationale: Jon names the deception explicitly: Mance's raids are feints designed to bait Marsh into dispersing the garrison. The wiki confirms this (prelude text). DEDUP check: `mance-rayder DISTRUSTS bowen-marsh` exists; `mance-rayder DECEIVES bowen-marsh` does NOT.
- status: NEW

**E-B-07**
- `mance-rayder` | MANIPULATES | `bowen-marsh` | tier=2
- qualifier: Mance's raiding-party strategy induces Marsh to march out, enabling the under-defended state Styr exploited
- evidence_ref: asos-jon-06.md:51
- quote: "The gate is here. The attack is here. . . . And Bowen Marsh has obliged him."
- rationale: MANIPULATES (inducing a strategic response) is a distinct edge from DECEIVES (which is about false belief). Both apply: Marsh was deceived about the real attack vector AND manipulated into the desired action. Tier-2 because Jon infers Mance's intent; the text doesn't have Mance explicitly stating "I will manipulate Marsh." DEDUP check: no `mance-rayder MANIPULATES bowen-marsh` in internal-edges.txt.
- status: NEW

**E-B-08**
- `mance-rayder` | DECEIVES | `nights-watch` | tier=1
- qualifier: concealed the existence and location of the Horn of Winter throughout the assault
- evidence_ref: asos-jon-10.md:165
- quote: "Did you think only crows could lie? I liked you well enough, for a bastard . . . but I never trusted you. A man needs to earn my trust."
- rationale: Mance reveals to Jon that Ygritte's claim ("they never found the horn") was a lie — Mance used disinformation to conceal his strategic reserve. This is active deception of the Watch and Jon specifically. DEDUP check: no `mance-rayder DECEIVES nights-watch` in internal-edges.txt.
- status: NEW

**E-B-09**
- `mance-rayder` | DECEIVES | `jon-snow` | tier=1
- qualifier: told Jon through Ygritte that he never found the Horn of Winter
- evidence_ref: asos-jon-10.md:163–165
- quote: "Ygritte said you never found the horn." / "Did you think only crows could lie?"
- rationale: Narrower than E-B-08 (Watch as institution): Jon personally was deceived by disinformation passed through Ygritte. The revelation at the parley is a specific call-back to Jon's earlier belief. Tier-1: the deception is explicitly confirmed in dialogue.
- status: NEW

### Thread 3: Scarecrow-sentinels ruse (Aemon's hidden-agency)

**E-B-10**
- `aemon-targaryen-son-of-maekar-i` | DECEIVES | `styr` | tier=1
- qualifier: devised the scarecrow-sentinel ruse to inflate the apparent garrison size
- evidence_ref: asos-jon-07.md:33–35
- quote: "The scarecrow sentinels," Donal Noye called them. . . . Whatever you called them, the straw soldiers had been Maester Aemon's notion."
- rationale: Aemon conceived the deception; Noye implemented it. The target (styr/wildlings) was explicitly the audience — "the hope was that the Thenns would see them from afar and decide that Castle Black was too well defended to attack." DEDUP check: no `aemon-targaryen-son-of-maekar-i DECEIVES styr` or any DECEIVES from Aemon in internal-edges.txt. The single existing DECEIVES edge is a different pairing entirely.
- status: NEW

**E-B-11**
- `aemon-targaryen-son-of-maekar-i` | DECEIVES | `mance-rayder` | tier=2
- qualifier: scarecrow-sentinel ruse targeted the whole wildling force, not only Styr's party
- evidence_ref: asos-jon-08.md:35
- quote: "So we know. We know how few you were, when you stopped the turtle."
- rationale: Mance's later admission that his skinchanger Varamyr "saw with eagle eyes" suggests he ultimately discovered the true numbers. But during the assault, the ruse was aimed at the wildling host. Tier-2 (Mance's eventual knowledge undercuts the deception's duration). Propose as complement to E-B-10 if the synthesizer wants to capture the wider target.
- status: NEW (lower priority — synthesizer may prefer to scope only to styr)

**E-B-12**
- `aemon-targaryen-son-of-maekar-i` | INFORMS | `lords-of-the-realm` | tier=1
- qualifier: Aemon sends ravens to four kings and dozens of lords (Stannis, Robb's bannermen, Iron Throne, etc.) warning of wildling attack — a hidden-lever play when Janos Slynt/Thorne held the Watch's chain of command
- evidence_ref: asos-jon-07.md:95
- quote: "Maester Aemon had sent a lot of birds . . . not to one king, but to four. . . . to the Umbers and the Boltons, to Castle Cerwyn and Torrhen's Square, Karhold and Deepwood Motte, to Bear Island . . ."
- rationale: This is a strategic hidden-agency beat: Aemon, operating outside the formal Watch command (Slynt/Thorne held authority), mobilizes the whole realm. The ravens are the reason Stannis comes. The INFORMS type may need a broad target; if `lords-of-the-realm` is not a graph node, propose node-prose on `aemon-targaryen-son-of-maekar-i` instead. Flag for synthesizer.
- status: NEW (target node may not exist — flag)

**E-B-13**
- `aemon-targaryen-son-of-maekar-i` | PROTECTS | `jon-snow` | tier=1
- qualifier: writes Cotter Pyke preventing Slynt from hanging Jon; protects him from trumped-up execution
- evidence_ref: asos-jon-09.md:199
- quote: "My lords, when Donal Noye was slain, it was this young man Jon Snow who took the Wall and held it . . . You are doing him a great wrong."
- rationale: DEDUP check: `aemon-targaryen-son-of-maekar-i PROTECTS jon-snow` [1] (asos-jon-09.md:135) ALREADY EXISTS in internal-edges.txt. Citing a different line (the tribunal defense speech) vs line 135 — but the edge-type and dyad are identical. This is a **DEDUP** with existing edge.
- status: DEDUP-EXISTS

### Thread 4: Who shot Ygritte? — SUSPECTED_OF analysis

**E-B-14 — CONTESTED ATTRIBUTION / REJECTED as SUSPECTED_OF**

The prose reads: "The arrow was black, Jon saw, but it was fletched with white duck feathers. Not mine, he told himself, not one of mine. But he felt as if it were." (asos-jon-07.md:191)

Jon's arrows are grey-goose-fletched (confirmed: asos-jon-07.md:115 — "the fletching grey"). The shooter used white duck feathers. Jon earlier wonders if Ygritte had shot at him with grey-goose fletched arrows during his escape (asos-jon-05.md:223). The white-duck-fletched arrow does NOT point to Jon. It also does NOT point to Ygritte's own side by text — white duck feathers are not attributed to any specific wildling archer in these chapters.

**DECISION: Do NOT mint a SUSPECTED_OF edge for any actor.** The text establishes only what the arrow is NOT (not Jon's), not what it is. No actor is named as a suspect, accused, or subject of suspicion by any POV character. Jon's guilt is emotional, not accusatory. Minting SUSPECTED_OF here would be inventing a suspect the text never introduces. This is a genuine open-attribution death — correct representation is node-prose on `ygritte-shot-at-castle-black` noting the arrow description and the unresolved attribution.

### Thread 5: Jon's parley as assassination sortie — hidden-agency

**E-B-15**
- `janos-slynt` | DECEIVES | `mance-rayder` | tier=1
- qualifier: sends Jon under false pretense of parley/treating while the actual mission is assassination
- evidence_ref: asos-jon-10.md:53
- quote: "We're not sending you to talk with Mance Rayder," Ser Alliser said. "We're sending you to kill him."
- rationale: Mance invited a parley envoy; Slynt exploits the parley framing to insert an assassin. The deception is aimed at Mance (the target of the false-flag envoy). Slynt and Thorne design the deception; Jon is the reluctant instrument. DEDUP check: no `janos-slynt DECEIVES mance-rayder` in internal-edges.txt.
- status: NEW

**E-B-16**
- `ser-alliser-thorne` | DECEIVES | `jon-snow` | tier=1
- qualifier: presented the parley mission as a chance to prove loyalty; the real purpose was an assassination the Watch would use either way — Jon killed Mance or Jon died trying
- evidence_ref: asos-jon-10.md:55
- quote: "Whether he slew Mance or only tried and failed, the free folk would kill him."
- rationale: Jon's internal understanding: the mission was a trap with no survivable outcome for him. Thorne frames it as loyalty-proving, but it's designed to dispose of Jon. Note: this is Jon's POV inference, not Thorne's stated intent — tier-2 is more appropriate.
- qualifier-revised: tier=2
- status: NEW

**E-B-17**
- `jon-snow` | DECEIVES | `janos-slynt` | tier=1
- qualifier: Jon goes to Mance intending to potentially destroy the Horn of Winter rather than simply deliver the assassination Slynt ordered
- evidence_ref: asos-jon-10.md:205
- quote: "If I can destroy the horn, smash it here and now . . . but before he could begin to think that through, he heard the low moan of some other horn"
- rationale: Jon independently conceives an alternate objective (destroy the horn) during the parley, diverging from Slynt's assassination order. He neither kills Mance nor reports the horn to Slynt afterward. This is a subtle deception-by-omission/divergent-agenda beat. Tier-1 because his internal intent is explicit in the text.
- status: NEW

**E-B-18**
- `janos-slynt` | MANIPULATES | `jon-snow` | tier=1
- qualifier: uses the ice cell + accusation of treason as leverage to coerce Jon into the assassination mission
- evidence_ref: asos-jon-10.md:20–22
- quote: "That old maester says I cannot hang you," Slynt declared. "He has written Cotter Pyke, and even had the bloody gall to show me the letter. . . . I will not have it said that Janos Slynt hanged a man unjustly. . . . I have decided to give you one last chance."
- rationale: Slynt's sequence is explicit manipulation: the execution threat is neutralized by Aemon, so Slynt substitutes a coercive "choice" (suicide mission vs. ice cell). Jon recognizes the trap. DEDUP check: no `janos-slynt MANIPULATES jon-snow` in internal-edges.txt.
- status: NEW

### Thread 6: Varamyr's surveillance — hidden intelligence layer

**E-B-19**
- `varamyr-sixskins` | SPIES_ON | `nights-watch` | tier=1
- qualifier: uses the eagle (Orell's former eagle, now his) to scout Castle Black's defenses from above during the siege
- evidence_ref: asos-jon-10.md:137–139
- quote: "I can soar above the Wall, and see with eagle eyes." / "So we know. We know how few you were, when you stopped the turtle. We know how many came from Eastwatch. We know how your supplies have dwindled."
- rationale: Mance's intelligence about Watch strength (numbers, supplies, the failed trebuchet) came from Varamyr's aerial reconnaissance via the eagle. This is explicit in Mance's speech. DEDUP check: no `varamyr-sixskins SPIES_ON nights-watch` or `varamyr-sixskins SPIES_ON castle-black` in internal-edges.txt. The cluster has SPIES_ON only once (jon SPIES_ON mance).
- status: NEW

**E-B-20**
- `varamyr-sixskins` | INFORMS | `mance-rayder` | tier=1
- qualifier: reports Watch's depleted numbers and supplies via eagle reconnaissance
- evidence_ref: asos-jon-10.md:139
- quote: "We know how few you were, when you stopped the turtle. We know how many came from Eastwatch. We know how your supplies have dwindled."
- rationale: INFORMS completes the loop: Varamyr surveils → informs Mance. DEDUP check: no `varamyr-sixskins INFORMS mance-rayder` in internal-edges.txt.
- status: NEW

### Thread 7: Aemon's command authority — hidden-agency during Watch leadership vacuum

**E-B-21**
- `aemon-targaryen-son-of-maekar-i` | INFORMS | `stannis-baratheon` | tier=1
- qualifier: Aemon's raven-network appeals to the kings ultimately reached Stannis (via Davos) and triggered the relief charge
- evidence_ref: asos-jon-11.md:109
- quote: "If not for my Hand, I might not have come at all. Lord Seaworth is a man of humble birth, but he reminded me of my duty . . . I had the cart before the horse, Davos said."
- rationale: Stannis came because of appeals — Davos converted the ravens' message into political action. A `REVEALS_TO` or `INFORMS` edge from Aemon to Stannis captures this causal chain. The baseline notes Aemon's letters as a "hidden lever" — this is the wiring. DEDUP check: `stannis-baratheon REVEALS_TO aemon-targaryen-son-of-maekar-i` [1] (affc-aemon-to-stannis, about Dany) already exists, but that is STANNIS→AEMON direction. The reverse `aemon INFORMS stannis` does NOT exist. Note: strictly the ravens went to multiple kings, and Davos is the intermediary — the synthesizer may prefer to route through `davos-seaworth`. Flag.
- status: NEW (flag: Davos as intermediary)

### Thread 8: Jon commands the Wall — legitimacy-without-title

**E-B-22**
- `donal-noye` | APPOINTS | `jon-snow` | tier=1
- qualifier: Noye delegates command of the Wall to Jon when he descends to hold the tunnel, creating an informal commander-in-chief role
- evidence_ref: asos-jon-08.md:81–82
- quote: "Jon, you have the Wall till I return." / "Lord? I'm a blacksmith. I said, the Wall is yours."
- rationale: Noye's explicit handover of command is a hidden-agency beat: a one-armed blacksmith with no formal title exercises and then delegates the Watch's supreme defensive authority, bypassing Slynt/Thorne/Wynton Stout entirely. `donal-noye TRUSTS jon-snow` exists; `donal-noye APPOINTS jon-snow` does NOT. The word "appoints" captures the explicit delegation.
- status: NEW

**E-B-23**
- `aemon-targaryen-son-of-maekar-i` | APPOINTS | `jon-snow` | tier=1
- qualifier: Aemon confirms/extends Noye's appointment after Noye's death, explicitly telling Jon he must lead
- evidence_ref: asos-jon-08.md:191
- quote: "You. You must lead." / "It must be you or no one. The Wall is yours, Jon Snow."
- rationale: After Noye dies, Aemon becomes the authority who formally presses Jon to command. `aemon-targaryen-son-of-maekar-i PROTECTS jon-snow` and `TUTORS jon-snow` exist; APPOINTS captures the explicit command-conferral. The phrasing "The Wall is yours" directly parallels Noye's handover. DEDUP check: `stannis-baratheon APPOINTS jon-snow` [1] (asos-jon-11, Stannis offers Winterfell) exists — but that is a completely different appointment. `aemon APPOINTS jon-snow` does NOT exist.
- status: NEW

---

## NOTES / UNCERTAINTIES

### Rejected / over-reading calls

1. **Ygritte SUSPECTED_OF shooting Deaf Dick Follard** — The text has Jon see Ygritte's red hair near Follard's body right after Follard is killed by a wildling archer (asos-jon-07.md:133). The proximity is notable but the POV text does NOT name Ygritte as the shooter. Jon glimpses her "not ten feet from Deaf Dick's body" but the arrow came from "the archer down below him." This is a missed shot (Jon tries to get her, fails), not an attribution. Do NOT mint SUSPECTED_OF. Recommend: harvest note only.

2. **Mance MANIPULATES bowen-marsh vs. DECEIVES** — Both E-B-06 and E-B-07 cover overlapping ground. The synthesizer should pick one or both. DECEIVES is clearly supported; MANIPULATES is inferential. If only one is minted, DECEIVES is the stronger call (Jon explicitly names it "feints").

3. **jon-snow SUSPECTED_OF killing ygritte** — This is a common fan framing, but the text explicitly exonerates Jon's arrows (white duck feathers ≠ Jon's grey goose). The *emotional* guilt is a MOURNS beat (already wired). Do NOT mint SUSPECTED_OF for Jon. The un-attributed nature of Ygritte's death is best represented in `ygritte-shot-at-castle-black` node prose.

4. **Satin DECEIVES wildlings (scarecrows)** — Satin positions the straw soldiers. But the conception and strategic deception was Aemon's; Satin is the executor, not the deceiver in any meaningful edge sense. Not worth minting separately.

5. **Mance WITHHOLDS Horn of Winter from his own people** — The text says "there are those among my people who want nothing more" (than to sound it). This is a political-internal deception toward his own host, not just the Watch. Could be `mance-rayder DECEIVES free-folk` (tier-2, Dalla's presence suggests the royal couple knew). Flagging as interesting but I lack a clean quote — recommend synthesizer decides.

6. **Rattleshirt LIES about jon killing Qhorin** — Rattleshirt's testimony to Slynt is false (he omits Qhorin's orders), a DECEIVES beat. But the Qhorin arc is Skirling Pass, not Castle Black proper. Out of scope for this dip per baseline scope-watch.

7. **Jon-snow REVEALS_TO stannis-baratheon (Horn of Winter)** — In asos-jon-11, Jon mentions having "brought us this magic horn" (Stannis's words). Jon did bring Stannis the horn from Mance's tent at the parley. But Stannis's speech attributes it to Jon, and Jon doesn't confirm or deny specifically. REVEALS_TO may be overstating Jon's active disclosure (vs. the horn simply being in his possession when Stannis arrived). Recommend node-prose on `mance-conceals-horn-of-winter` noting its recovery.

### Scope boundary notes

- Varamyr's post-death skinchanging (ADWD) is out of scope.
- The Mance IMPERSONATES lord-of-bones glamour (ADWD) is already wired — confirmed.
- `fight-at-the-fist` vs `battle-of-the-fist-of-the-first-men` possible dup: flagged per baseline; not touched here.

---

## HARVEST

- asos-jon-05.md:81 / vivid-description / Ygritte kisses Jon in front of the raiding column — "All men must die, Jon Snow. But first we'll live." — load-bearing quote for Jon/Ygritte relationship arc
- asos-jon-05.md:223 / foreshadowing / Jon examines the arrow from his thigh — grey or white fletching? — seeds the Ygritte-shot ambiguity resolved in asos-jon-07
- asos-jon-06.md:19 / food+hospitality / Jon at Mole's Town stable: stableboys give him wine skin and half a loaf of brown bread — hospitality under urgent conditions
- asos-jon-07.md:73–82 / food / Owen delivers buns (raisins, pine nuts, dried apple), wheel of cheese, bag of onions, crock of butter — possible last meal before battle; grim register
- asos-jon-07.md:101 / food (siege) / "Near evenfall, Owen the Oaf returned with a loaf of black bread and a pail of Hobb's best mutton, cooked in a thick broth of ale and onions. . . . They ate every bit of it, using chunks of bread to wipe the bottom of the pail." — siege warmth, comradeship before battle
- asos-jon-08.md:25 / food (siege) / "Three-Finger Hobb passed out chunks of black bread" — sparse siege ration while waiting in the Wall cage
- asos-jon-08.md:85 / food (siege) / "Hobb rode up the chain with cups of onion broth, and Owen and Clydas served them to the archers where they stood, so they could gulp them down between arrows" — extraordinary image: hot broth served mid-battle on top of the Wall
- asos-jon-09.md:51 / food (siege/last meal frame) / "So it was that Jon had a belly full of bread, bacon, onions, and cheese when he heard Horse shout, 'IT'S COMING!'" — Jon forces himself to eat before final turtle assault
- asos-jon-08.md:171 / quote / "I am the last of the giants" — Jon's reaction to finding Mag the Mighty dead; load-bearing elegiac quote for the Mag/Noye event node
- asos-jon-07.md:205 / quote / "You know nothing, Jon Snow" — Ygritte's death line; already known but line reference confirmed: asos-jon-07.md:205
- asos-jon-10.md:281 / description / Stannis's banners: seahorse, ring of flowers, yellow with red device — arrival scene; potentially useful for heraldry index
- asos-jon-05.md:87 / foreshadowing-geography / the Wall descent at Greyguard (abandoned 200 years, collapsed stairs) — first confirmation of the southern infiltration route Styr used
- asos-jon-09.md:47 / food (starvation register) / Mole's Town entirely deserted; Zei sent for villagers never returns — civilian flight signals the siege's impact on the civilian population
- asos-jon-11.md:61 / quote / Stannis on Noye: "Noye made my first sword for me, and Robert's warhammer as well. Had the god seen fit to spare him, he would have made a better Lord Commander than any of these fools squabbling over it now." — strong characterization quote for noye node
