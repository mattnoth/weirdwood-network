# Fresh Verification — Battle of Castle Black Enrichment Dip
**Session:** S153 | **Verifier:** independent (no prior involvement) | **Date:** 2026-06-26

---

## Priority 1 — Interpretive / Causal / Whodunit Edges

### E03 | `styr VICTIM_IN southern-thenn-assault-on-castle-black`
**Verdict: CONFIRM**

Text is unambiguous: *"Twenty-odd Thenns were still huddled together between the fires when the ice
cracked from the heat, and the whole lower third of the stair broke off, along with several tons of
ice. That was the last that Jon Snow saw of Styr, the Magnar of Thenn. The Wall defends itself, he
thought."* (ASOS Jon VII) Styr is last seen climbing the barricade, surveying, then next referenced in
the context of the fire/ice trap as part of those twenty-odd — he disappears into the collapse. Tormund
in Jon X confirms Styr never made it out ("He was going to bring the whole Wall down." / "Har! ... I
never had much use for Styr."). The kill mechanism is the fire/ice collapse, not Jon personally.

**Was it right NOT to mint `jon KILLS styr`?** Yes, confirmed. Jon does not personally kill Styr.
Jon's role is triggering the fire (fire arrows at the oil-soaked stair), but the Wall/fire/ice
collapse does the actual killing. The POV text reinforces this with *"The Wall defends itself."*
Styr's death is the Wall's work, not Jon's. Decision upheld.

Citation: ASOS Jon VII (asos-jon-07.md, line 181)

---

### E24 | `janos-slynt MANIPULATES jon-snow` (qualifier: via_threat)
**Verdict: ADJUST**

The text supports coercion but the mechanism is threat-of-death-in-the-ice-cell, not threat in the
abstract. Slynt says: *"If you are too craven to face this turncloak king, we can return you to your
ice cell. This time without the furs, I think."* (ASOS Jon X) This is squarely a threat — Slynt
threatens to kill Jon by freezing in lieu of being able to hang him (Aemon blocked the hanging). So
`via_threat` is defensible.

However, scrutinize the MANIPULATES label itself. MANIPULATES implies deception or false framing.
What actually happens here is explicit coercion — an open threat with an ultimatum. There is no
deception in Slynt's *threat*; the deception is in the framing of the mission as a "parley" (which is
more Thorne's layer). Slynt's direct action is COERCES, not MANIPULATES in the strict sense.

Recommended adjustment: if the graph vocabulary has a COERCES edge type, prefer it. If MANIPULATES is
the closest available type, retain it but change the qualifier from `via_threat` to `via_coercion` to
distinguish this from information-manipulation. If the vocabulary is rigid (MANIPULATES only with
qualifier enums), then `via_threat` is acceptable as a fallback.

Check: does Alliser Thorne have a stronger claim to the MANIPULATES label? Thorne frames the parley
cover and says *"We're not sending you to talk with Mance Rayder. We're sending you to kill him."*
Both are complicit; Slynt issues the ultimatum, Thorne supplies the strategic framing. The current
edges (E22 COMMANDS_IN Thorne, E24 MANIPULATES Slynt) split this correctly — Slynt does the
coercive ultimatum, Thorne does the commands. The edge assignment is directionally right; the label
is borderline-defensible with a qualifier adjustment.

Citation: ASOS Jon X (asos-jon-10.md, lines 19–43)

---

### E27 | `bowen-marsh-marches-the-garrison-from-castle-black ENABLES attack-on-castle-black`
**Verdict: CONFIRM**

The causal logic is sound and textually supported. Jon states directly: *"Feints. Mance wants us to
spread ourselves thin, don't you see? And Bowen Marsh has obliged him."* (ASOS Jon VI) The resulting
garrison is explicitly characterized as *"old men, cripples, and green boys"* — the very condition
that makes the assault viable. Mance himself confirms in Jon X: *"I drew your garrison away with
feints and raids and secondary attacks. Bowen Marsh swallowed that lure as I knew he would."* This is
not over-distal; it is the stated enabling precondition, confirmed by both POV character and the
antagonist. ENABLES (not CAUSES) is the right type — Marsh's departure creates the necessary
condition, but Mance's command is the proximate cause.

Citation: ASOS Jon VI (asos-jon-06.md, lines 51–52); ASOS Jon X (asos-jon-10.md, line 171)

---

### E28 | `mance-rayder MANIPULATES bowen-marsh` (qualifier: via_false_information)
**Verdict: CONFIRM**

Supported by both Jon's inference in Jon VI and Mance's explicit confession in Jon X. Mance: *"I
drew your garrison away with feints and raids and secondary attacks. Bowen Marsh swallowed that lure
as I knew he would."* (Jon X) The mechanism is feints (false threat signals along the Wall), which
is `via_false_information` — Mance manufactured a picture of distributed threat that was
strategically false as a whole, inducing Bowen to disperse. This is genuine manipulation, not merely
a threat. `via_false_information` is the correct qualifier. Tier-2 is appropriate (inferred from
Mance's admission + Jon's real-time analysis, but not a single unambiguous POV moment of Marsh
being deceived).

Citation: ASOS Jon VI (line 51); ASOS Jon X (line 171)

---

### E29 | `fight-at-the-fist ENABLES attack-on-castle-black`
**Verdict: CONFIRM (with note)**

The causal logic is textually supported. Jon VI explicitly states: *"Two hundred men had left Castle
Black with Lord Commander Mormont, two hundred of the Watch's best."* Only a dozen returned from the
Fist. This gutting of Castle Black's fighting strength is the upstream precondition for why the castle
can be threatened with ~120 Thenns. The edge is inferred rather than stated as a direct causal link,
but the inference is tight and unavoidable — without the Fist losses, Marsh's departure still leaves a
viable garrison; with them, it does not.

Tier-2 is correct for an inferred precondition. ENABLES is the right type (not CAUSES — the Fist
didn't cause the attack, it made the attack viable). Not too distal: the Fist directly caused the
Watch's strength to collapse, which is the structural reason Castle Black can be attacked at all.

Note: the node-prose for `bowen-marsh-marches-the-garrison-from-castle-black` references Bowen
leaving "old men, cripples, and green boys" — the Fist is the upstream reason *why* Bowen's
departure leaves so few, making E29 and E27 a legitimate two-step causal chain (Fist → Bowen's
departure hurts more → attack viable). Both edges are warranted.

Citation: ASOS Jon VI (asos-jon-06.md, line 97)

---

### E30 | `fight-at-the-fist MOTIVATES mance-rayder`
**Verdict: CONFIRM (with precision note)**

Mance in Jon X: *"You saw the Fist of the First Men. You know what happened there. You know what we
are facing... They grow stronger as the days grow shorter and the nights colder."* Mance confirms that
the Others' demonstrated threat (epitomized at the Fist) is *why* he is trying to break the Wall and
bring his people south — not for conquest, but for survival: *"I've come with my tail between my
legs to hide behind your Wall."* MOTIVATES (event→person) is the right type: the Fist event motivates
Mance's entire strategic goal. This is not agency-collapse — Mance is the agent who chooses how to
respond; the Fist is the motivating condition.

Precision note: the Fist is one among several cumulative demonstrations (the Others' increasing
attacks on free folk), but it is the specific event cited by Mance as the context for his explanation
to Jon. Tier-2 is appropriate (Mance's stated motivation is Others-driven, and the Fist is the
canonical example, but he doesn't say "the Fist specifically caused me to march").

Citation: ASOS Jon X (asos-jon-10.md, lines 179–183)

---

### E32 | `mance-rayder DECEIVES jon-snow`
**Verdict: CONFIRM**

The Horn of Winter lie is textually precise. Jon recalls: *"Mance never found the horn, though,
that's something. The Horn of Winter, that's what he was digging for."* (Jon VI, Jon quoting his own
report to Noye — this is what Ygritte told him). In Jon X Mance reveals: *"Did you think only crows
could lie? I liked you well enough, for a bastard . . . but I never trusted you."* Jon's information
from Ygritte that Mance never found the horn is confirmed to be a lie Mance planted/permitted. The
deception is via Ygritte (indirect channel). DECEIVES is the correct type. Tier-1 is supportable —
this is a textually confirmed lie, not an inference.

Note: the deception channel runs Mance → (via Ygritte) → Jon. The edge as modeled goes directly
Mance→Jon (DECEIVES), which is the correct direction for agency. The intermediate channel (Ygritte)
doesn't need its own edge here.

Citation: ASOS Jon VI (line 119); ASOS Jon X (line 165)

---

### E34 | `varamyr SPIES_ON nights-watch` + E35 | `varamyr INFORMS mance-rayder`
**Verdict E34: CONFIRM | Verdict E35: CONFIRM (with caveat)**

**E34:** Varamyr's eagle aerial recon is explicitly stated: *"And I can soar above the Wall, and see
with eagle eyes."* (Jon X, Varamyr directly). SPIES_ON nights-watch is the correct type and
direction.

**E35:** Mance immediately follows up: *"We know how few you were, when you stopped the turtle. We
know how many came from Eastwatch. We know how your supplies have dwindled."* (Jon X) This is Mance
stating what he learned from the recon. The INFORMS edge (Varamyr→Mance) is the logical flow and
Mance attributes "We know" to collective intelligence that includes Varamyr's eagle (he says "So we
know" immediately after Varamyr's boast). Both edges correct.

Caveat on tier: both are tier-1 in the candidates.json — this is defensible for E34 (Varamyr states
it directly in POV), and for E35 the inference is tight enough to be tier-1 (Mance's "We know"
follows directly from Varamyr's statement). No adjustment needed.

Citation: ASOS Jon X (asos-jon-10.md, lines 137–139)

---

### E36 | `aemon-targaryen-son-of-maekar-i DECEIVES styr`
**Verdict: ADJUST**

The scarecrow-sentinel ruse is textually supported: *"The hope was that the Thenns would see them
from afar and decide that Castle Black was too well defended to attack."* (Jon VII) Aemon is credited
with the idea: *"Whatever you called them, the straw soldiers had been Maester Aemon's notion."*

However, two issues:

1. **Target:** Styr is not specifically identified as the target of the deception — the hope is the
   Thenns (as an attacking force) would be deterred. Styr is the commander of the Thenns, so
   DECEIVES→styr is a reasonable synecdoche (you deceive the commander of a force), but the text
   aims the deception at the Thenns broadly. The node-prose acknowledges "to deter the Thenns" but
   the edge points to Styr specifically. This is borderline: Styr is the decision-maker who would
   judge the apparent garrison strength, so he is the relevant target. Retain but acknowledge the
   proxy.

2. **Effectiveness:** The ruse does not work — the Thenns attack anyway (Jon VII: *"more likely the
   wildlings had simply paused for a bit of rape and plunder in Mole's Town. Or maybe Styr was
   waiting for nightfall."*). The Thenns still assault. DECEIVES implies a successful deception.
   The ruse *fails* to deter Styr. This is a meaningful problem. If the deception doesn't land, the
   edge may be a false claim.

**Recommended adjustment:** Change the edge to ATTEMPTS_TO_DECEIVE if such a type exists, or
annotate with qualifier `unsuccessful`. If the vocabulary doesn't support attempted-but-failed
deception, REJECT this edge — a DECEIVES edge asserts the deception succeeded, and it didn't: the
Thenns attacked. The scarecrow ruse is better captured in node-prose as a tactical attempt, not a
successful deceptive act.

**Verdict: ADJUST** — either add `outcome: unsuccessful` / `qualifier: attempted` OR REJECT if the
vocabulary doesn't support this nuance. The ruse's existence is real; the DECEIVES label overclaims.

Citation: ASOS Jon VII (asos-jon-07.md, lines 33–35)

---

## Priority 2 — Node Justification

### `southern-thenn-assault-on-castle-black`
**Verdict: KEEP**

This is a distinct narrative event with its own arc (Mance's southern pincer, Jon's warning, the
barricade defense, the burning stair, Styr's death). It is a separately-named prong of the larger
battle, has multiple participants and sub-beats, and warrants reification. SUB_BEAT_OF
attack-on-castle-black is correct.

---

### `death-of-ygritte`
**Verdict: KEEP**

Textually important and emotionally load-bearing. The shooter attribution is handled correctly in
node-prose (un-attributed black arrow with white duck feathers — *"Not mine . . . not one of mine"*).
No KILLS/SUSPECTED_OF edge is correct. Node-prose correctly notes Jon's later "My brother" to
Tormund (Jon X, line 107) without overclaiming an identification. SUB_BEAT_OF
southern-thenn-assault-on-castle-black is correct (she dies in the aftermath of that battle, under
the Lord Commander's Tower).

---

### `noye-and-mag-die-in-the-tunnel`
**Verdict: KEEP**

Good reification. The mutual-death is one of the battle's defining tragic moments, Tormund
memorializes it explicitly in Jon X ("Donal Noye, and Mag the Mighty — Har! That must o' been a
fight to see"). This event earns its own node. Pre-existing Noye↔Mag KILLS dyad correctly retained;
this node adds the queryable event hub. Node-prose quote *"I don't know who died first"* is included
— strong.

---

### `jon-takes-command-of-the-wall`
**Verdict: KEEP**

Two distinct APPOINTS moments (Noye before descending, Aemon after Noye dies) make this a real
event beat, not just node-prose. The Noye handoff and Aemon confirmation are narratively separate and
both carry load. Correct to reify. SUB_BEAT_OF attack-on-castle-black is correct.

---

### `jon-sortie-to-mance-camp`
**Verdict: KEEP (with minor scrutiny)**

The sortie occupies the entirety of ASOS Jon X and involves Jon walking into Mance's camp with
Longclaw intending to kill him, the Horn of Winter reveal, and Stannis's arrival cutting the sortie
short. This is a substantial discrete event beat, not just an edge. SUB_BEAT_OF
attack-on-castle-black is correct — it is the final beat of the battle sequence (before Stannis
interrupts). Tier-2 on the SUB_BEAT_OF is appropriate since the sortie is Jon's POV-chapter action
taken under orders from Slynt/Thorne, not a conventional "battle" sub-beat, but it is still
chronologically part of the extended battle arc.

---

### `bowen-marsh-marches-the-garrison-from-castle-black`
**Verdict: KEEP (barely)**

This is the weakest of the six nodes — it is a background event that precedes the battle, not a
moment the reader directly witnesses. Bowen Marsh's departure is reported retrospectively (Jon learns
from Noye: "Everywhere... defending the Wall against your wildling friends"). It is never a direct
POV scene. The question is whether this warrants a node vs. node-prose on bowen-marsh's own node.

However: it has a named agent (Bowen Marsh), a named mechanism (feint-induced dispersal), a real
strategic consequence (enabling the attack), and is cited twice across two chapters. It is the
upstream ENABLES edge and anchors the MANIPULATES edge from Mance. Reifying it as an event makes
both of those edges queryable. KEEP, but this is the node most at risk of being folded into
bowen-marsh's node-prose in a future tightening pass.

---

## Priority 3 — Role Edges (Lighter Check)

**E01:** `southern-thenn-assault SUB_BEAT_OF attack-on-castle-black` — CONFIRM. The southern assault
is a prong of the battle.

**E02:** `styr COMMANDS_IN southern-thenn-assault` — CONFIRM. Styr is definitively the Magnar
commanding the southern force.

**E04:** `jon-snow AGENT_IN southern-thenn-assault` — CONFIRM. Jon directs the King's Tower defense.

**E05:** `satin AGENT_IN southern-thenn-assault` — CONFIRM. Satin pours boiling oil with Jon (Jon
VII, line 145).

**E06:** `donal-noye COMMANDS_IN southern-thenn-assault` — CONFIRM. Noye prepares the oil-drenched
stair trap and commands the broader defense. The quote captures his preparation; he commands both the
barricade and the stair trap (Jon VII, lines 179–181).

**E07:** `longclaw WIELDED_IN southern-thenn-assault` — CONFIRM. Jon uses Longclaw against the first
Thenn through the trapdoor (Jon VII, line 145).

**E08:** `death-of-ygritte SUB_BEAT_OF southern-thenn-assault` — CONFIRM. Ygritte dies in the
aftermath, same chapter.

**E09:** `ygritte VICTIM_IN death-of-ygritte` — CONFIRM.

**E10:** `jon-snow WITNESS_IN death-of-ygritte` — CONFIRM. Jon holds her as she dies.

**E11:** `noye-and-mag-die-in-the-tunnel SUB_BEAT_OF attack-on-castle-black` — CONFIRM. The tunnel
fight is a separate sub-beat from the southern assault, correctly under the parent battle.

**E12:** `donal-noye AGENT_IN noye-and-mag-die-in-the-tunnel` — CONFIRM. Noye's sword in the
giant's throat.

**E13:** `donal-noye VICTIM_IN noye-and-mag-die-in-the-tunnel` — CONFIRM. Giant crushed his spine.

**E14:** `mag-mar-tun-doh-weg AGENT_IN noye-and-mag-die-in-the-tunnel` — CONFIRM. Mag wrenches bars,
kills Spotted Pate, crushes Noye.

**E15:** `mag-mar-tun-doh-weg VICTIM_IN noye-and-mag-die-in-the-tunnel` — CONFIRM. Noye's sword in
his throat.

**E16:** `jon-takes-command SUB_BEAT_OF attack-on-castle-black` — CONFIRM.

**E17:** `jon-snow AGENT_IN jon-takes-command` — CONFIRM.

**E18:** `donal-noye APPOINTS jon-snow` — CONFIRM. Noye's handoff before descending to the tunnel.

**E19:** `aemon-targaryen APPOINTS jon-snow` — CONFIRM. Aemon's confirmation after Noye dies.

**E20:** `jon-sortie SUB_BEAT_OF attack-on-castle-black` — CONFIRM (tier-2 appropriate).

**E21:** `jon-snow AGENT_IN jon-sortie` — CONFIRM.

**E22:** `janos-slynt COMMANDS_IN jon-sortie` — CONFIRM. Slynt issues the order.

**E23:** `alliser-thorne COMMANDS_IN jon-sortie` — CONFIRM. Thorne states the assassination purpose.

**E25:** `longclaw WIELDED_IN jon-sortie` — CONFIRM. Jon carries Longclaw into the camp.

**E26:** `bowen-marsh AGENT_IN bowen-marsh-marches-the-garrison` — CONFIRM.

**E31:** `jon-snow DECEIVES styr` — CONFIRM. Jon explicitly *"lied where he dared and feigned
ignorance a few times"* (Jon V, line 93) when Styr questioned him about Castle Black's defenses
during the march south. This is a clear, stated deception. Tier-1 is appropriate. The quote is the
right one.

**E33:** `jon-snow REVEALS_TO donal-noye` — CONFIRM. Jon's warning in Jon VI (*"There are wildlings
south of the Wall, coming up from Queenscrown to open the gate"*) is the intelligence that enables
the defense. REVEALS_TO is the correct type.

**E37:** `mance-rayder OWNS horn-of-winter` — see Theory-Gate section.

**Overall role edges:** No direction reversals, no miscast roles. Role edges are clean.

---

## Priority 4 — Negative Decisions

### `jon-snow KILLS styr` — NOT minted
**Verdict: CORRECT**

Confirmed above under E03. The Wall/fire/ice collapse kills Styr; Jon's role is triggering the
burning stair. No personal kill.

---

### Ygritte's death — no attacker edge
**Verdict: CORRECT**

The text is deliberate: *"The arrow was black, Jon saw, but it was fletched with white duck feathers.
Not mine, he told himself, not one of mine."* (Jon VII) Jon later tells Tormund only *"My brother"*
(Jon X), meaning a Night's Watch man — never named. The text intentionally withholds attribution.
Node-prose is the right call. SUSPECTED_OF would require a specific suspected agent; the text names
no one. There is no candidate specific enough to hang a SUSPECTED_OF on. This is the rare case where
the author wants the reader to feel the ambiguity. No edge is correct.

---

### No "Grenn holds the gate" node
**Verdict: CORRECT**

Book text: Noye specifically selects *four* men to go with him to the tunnel: *"Jon, you have the
Wall till I return... I need two bows and two spears to help me hold the tunnel if they break the
gate. More than ten stepped forward, and the smith picked his four."* (Jon VIII) Those four are
unnamed in the POV. Grenn is up on the Wall with Jon at this point (he rolls oil barrels with Pyp on
the Wall; Jon explicitly says "Grenn, you have the Wall" when departing). Grenn never goes to the
tunnel in the book — the HBO scene of Grenn holding the gate against Mag is television invention.
No node warranted.

---

## Theory-Gate

### E37 | `mance-rayder OWNS horn-of-winter` (tier-1)
**Verdict: CLEAN**

The edge asserts only possession — Mance has the horn. The node body (`horn-of-winter`) is not
included in this dip's new nodes, so I verify the `jon-sortie` node-prose instead. The node for
`jon-sortie-to-mance-camp` describes: *"Jon walks into the camp with Longclaw, is brought before
Mance, sees the Horn of Winter."* No assertion about the horn's powers. The `southern-thenn-assault`
node mentions *"the Wall defends itself"* but this refers to the fire/ice collapse, not the horn.

The text in Jon X has Mance say *"If I sound the Horn of Winter, the Wall will fall. Or so the songs
would have me believe."* The hedging (*"or so the songs would have me believe"*) and Dalla's
sorcery-warning are in the text; the dip does NOT assert the horn works. The new node-prose does not
claim the horn actually wakes giants or brings down the Wall. The `horn-of-winter` node (which
predates this dip) is what would contain any such claim — that node is not modified here.

The OWNS edge (Mance possesses it) is tier-1 — the horn's physical presence in Mance's tent is
directly shown in POV, confirmed verbally by Mance. Theory-gate is clean: no leaked assertion that
the horn is functional or that Joramun-provenance is confirmed.

---

## Summary

**Tallies:** 35 CONFIRM / 1 ADJUST (E24) / 1 ADJUST-OR-REJECT (E36) / 0 outright REJECT

**E24 (MANIPULATES via_threat):** Edge is defensible; qualifier should shift to `via_coercion` if
vocabulary supports it. The coercion is open/explicit rather than manipulative in the strict sense.
Low severity.

**E36 (DECEIVES styr — scarecrow ruse):** The ruse fails to deter Styr — the Thenns attack anyway.
DECEIVES overclaims a successful deception. This is the single biggest concern in the dip. Either
add `outcome: unsuccessful` / `qualifier: attempted`, or REJECT the edge and move the ruse to
node-prose only (it already appears in `southern-thenn-assault-on-castle-black`'s node body). If the
vocabulary supports an attempted-deception marker, ADJUST; if not, REJECT to avoid a false claim.

**Node layer:** All 6 nodes are warranted. `bowen-marsh-marches-the-garrison-from-castle-black` is
the weakest but earns its place as the anchor for E27 and E28.

**Negative decisions:** All three (no jon-kills-styr, no Ygritte attacker, no Grenn-holds-gate) are
correct per the book text.

**Theory-gate:** CLEAN. E37 asserts possession only; no theory leak.

**Biggest single concern:** E36 — DECEIVES asserts success, but the scarecrow ruse did not deter
Styr. This should be resolved before the dip is committed: either add a qualifier that marks the
attempt as unsuccessful, or drop the edge and keep the ruse as node-prose.
