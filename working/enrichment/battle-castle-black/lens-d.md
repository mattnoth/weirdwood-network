# Lens D — existing-node ↔ existing-node causal wiring — proposals

> Analyst: Lens D (existing-node ↔ existing-node causal wiring)
> Session: S153 (assigned)
> Dip scope: Battle of Castle Black (ASOS Wall defense)
> Dedup baseline: internal-edges.txt (180 internal edges checked)

---

## PROPOSED CAUSAL EDGES

**D1 — The marquee upstream gap: Watch garrison wiped out → Mance attacks Castle Black**

- `fight-at-the-fist` | ENABLES | `attack-on-castle-black` | tier=2 | evidence_ref=asos-jon-08.md:55 | quote="Having learned that the bulk of the Watch's fighting force has been wiped out in the fight at the Fist by the Others, Mance Rayder plans to lead his main host through the gate in the Wall by Castle Black." | rationale=Attack-on-castle-black's own Origins prose names the Fist as the direct precondition: the wiped-out garrison is WHY Mance judges the castle vulnerable. This is the classic ENABLES shape (precondition, not mechanical causation). Quote is from node prose but mirrors asos-jon-08.md:55 where Noye's scarcity ("forty odd" left) is dramatized. Verbatim book: asos-jon-06.md line 65: "Forty odd," said Donal Noye. "The crippled and infirm, and some green boys still in training." (inferred causal connection; node prose states causation explicitly) | status=NEW

**D2 — Mance's feint raids drain the garrison out of Castle Black (no node for the march itself, but the chain is wirable at the hub level)**

*DEPENDENCY NOTE: Bowen Marsh marching the garrison north is NOT a separate node — it is described only inside attack-on-castle-black's Origins prose. There is no `bowen-marsh-marches-garrison` or `mance-sends-raiding-parties` node. This is a lens-A gap (build the event node), not a lens-D seam I can wire. See NOTES.*

**D3 — Queenscrown refusal MOTIVATES Jon's escape and warning (Queenscrown → Jon-warns-Castle-Black)**

*DEPENDENCY NOTE: There is no `jon-escapes-the-raiders` or `jon-warns-castle-black` node — the warning ride is described in asos-jon-06 but has no event hub. The causal chain (Queenscrown → escape → warning → defense preparations) cannot be wired until lens A mints the escape node. See NOTES.*

**D4 — Jon's refusal at Queenscrown ENABLES Mance's southern assault losing surprise**

- `jon-refuses-to-kill` | ENABLES | `attack-on-castle-black` | tier=2 | evidence_ref=asos-jon-07.md:13 | quote="Styr had lost all hope of taking Castle Black unawares when Jon escaped him, yet even so, he need not have warned of his approach so bluntly." | rationale=Jon's refusal to kill the old man (asos-jon-05) was the crack that let him escape at Queenscrown, and asos-jon-07 explicitly states Styr lost the element of surprise because of Jon's escape. The refusal is the root node in the chain. ENABLES = precondition (his refusal is what made the escape possible, which made surprise impossible). Agency pathway preserved: Jon refused → Jon escaped → Jon warned → surprise lost. Not an agency-collapse (Jon chose to refuse). | status=NEW

**D5 — Jon-spares-ygritte ENABLES Jon-refuses-to-kill (Skirling-Pass → Queenscrown moral chain)**

*Considered and rejected — see NOTES D5. The two events are causally adjacent but the link is dispositional/character-arc, not a structural precondition. jon-spares-ygritte is ACOK; jon-refuses-to-kill is ASOS. A MOTIVATES edge is plausible but speculative — the text does not invoke the prior mercy as the reason for the refusal. Leaving as a NOTE.*

**D6 — attack-on-castle-black CAUSES battle-beneath-the-wall — UPGRADE PROPOSAL**

Current edge: `attack-on-castle-black CAUSES battle-beneath-the-wall` [tier-3, weak quote: "They must take the gate, or they cannot pass."] (asos-jon-08.md:55). That quote explains WHY the gate matters but doesn't directly state that the attack caused the battle beneath. A stronger cite exists in the Aftermath prose of the attack-on-castle-black node: "Knowing Mance Rayder and his main force are coming, the Night's Watch begins to prepare for the battle beneath the Wall." And in asos-jon-10.md:287 Stannis arrives mid-sortie.

The best direct chain-statement is in asos-jon-08.md where Noye says "They must take the gate, or they cannot pass" — this is the articulation of the mechanism, but CAUSES (not just mechanism) is stated implicitly not verbatim. Tier-3 is defensible; tier-2 upgrade requires a verbatim statement of causation.

Recommended: upgrade to tier-2, replace with a better cite from the attack-on-castle-black node prose (which is wiki-sourced tier-2 authority), and add a book-provenance cite from asos-jon-08.md:55. The current quote is adequate but the cite framing is weak.

- `attack-on-castle-black` | CAUSES | `battle-beneath-the-wall` | tier=2 | evidence_ref=asos-jon-08.md:55 | quote="They must take the gate, or they cannot pass." | rationale=UPGRADE from tier-3: the wiki Origins for attack-on-castle-black explicitly states "Knowing Mance Rayder and his main force are coming, the Night's Watch begins to prepare for the battle beneath the Wall" — the southern assault is what confirmed the northern assault was imminent, triggering preparations. The current quote is adequate; upgrade the tier confidence. | status=UPGRADE

**D7 — Jon-commands-defense-of-the-Wall ENABLES jon-elected-lord-commander (in-battle command transfer)**

The question posed in the brief: after Noye dies, Jon commands the Wall — does that merit a ENABLES edge to his election?

`battle-beneath-the-wall ENABLES jon-elected-lord-commander` already exists (asos-jon-12.md:41). The in-battle command transfer (Noye delegates → Jon leads → Jon proves himself) is captured *inside* that existing edge's causal chain. There is no separate node for "Jon takes command of the Wall defense" — it is narrated in asos-jon-08.md:82-191 as a single continuous arc.

The text in asos-jon-08.md:191 is very direct: Maester Aemon says "You. You must lead." and "The Wall is yours, Jon Snow." This is the command-transfer beat. There is also no node for the post-Noye command period. This is a lens-A gap. A MOTIVATES edge from the Aemon speech to jon-elected-lord-commander could be proposed, but Aemon's exhortation ("The Wall is yours, Jon Snow") is a *within-chapter* beat, not an existing event node.

*No new lens-D seam here — the existing `battle-beneath-the-wall ENABLES jon-elected-lord-commander` edge already covers the full battle-to-election chain. Finer granularity requires a new "Jon takes command of the Wall" event node (lens A).*

**D8 — Jon-sortie-to-Mance ENABLES battle-beneath-the-wall (was the sortie a precondition for Stannis's arrival?)**

Checked: Jon's assassination sortie (asos-jon-10) does NOT enable Stannis's arrival — Stannis was already en route independently (stannis-moves-to-the-wall CAUSES battle-beneath-the-wall already wired). Jon happens to be in the wildling camp when Stannis arrives; the timing is coincidence, not causation. No seam.

**D9 — fight-at-the-fist MOTIVATES mance-rayder (Fist MOTIVATES Mance to attack Castle Black)**

The Fist-to-attack chain can also be expressed as a MOTIVATES edge on Mance (the person who decided to press the attack). The text in asos-jon-10.md:179-182 is explicit: Jon asks "If you've had the Horn of Joramun all along, why haven't you used it?" and Mance explains his people have bled enough from the Others — the Others at the Fist are his stated reason for marching south. But MOTIVATES requires a person/house as target. `mance-rayder` is a character node. This is a valid second seam complementing D1.

- `fight-at-the-fist` | MOTIVATES | `mance-rayder` | tier=2 | evidence_ref=asos-jon-10.md:183 | quote="They grow stronger as the days grow shorter and the nights colder. First they kill you, then they send your dead against you. The giants have not been able to stand against them, nor the Thenns, the ice river clans, the Hornfoots." | rationale=Mance explicitly cites the Others' growing strength (demonstrated at the Fist and in subsequent losses) as WHY he is marching south. This is a clean MOTIVATES (Fist-defeat → Mance decides to seek safety behind the Wall). Preserves agency: Mance CHOSE to march south, the Fist-loss MOTIVATED that choice. Note "inferred" — the text does not say "the Fist caused me to march" verbatim; Mance describes the ongoing Others threat, of which the Fist was the catalytic demonstration. tier-2. | status=NEW

---

## RECOMMENDED RETIREMENTS (junk PRECEDES / wrong edges)

- `attack-on-castle-black` | PRECEDES | `battle-near-yunkai` | why retire: Pure cross-theater chronology artifact — these events are in two different storylines (Wall / Essos), thousands of miles apart. The PRECEDES link is a calendar coincidence, not a causal or narrative connection. Junk edge, retire.

- `battle-at-the-burning-septry` | PRECEDES | `attack-on-castle-black` | why retire: Same issue — burning-septry is a Hound/Brotherhood event in the Riverlands; its PRECEDES connection to Castle Black is a calendar artifact with no causal or narrative relevance. Retire.

---

## NOTES / UNCERTAINTIES

**D1 cite clarification**: The best verbatim book support for the fight-at-the-fist → attack-on-castle-black ENABLES link is:
- asos-jon-06.md:65 (Noye, forty men left — dramatizes the weakness)
- asos-jon-06.md:51 (Jon on the feints: "Feints. Mance wants us to spread ourselves thin, don't you see? And Bowen Marsh has obliged him. The gate is here. The attack is here.")
- wildlings-attack-the-gate's existing SUB_BEAT_OF quote: "Having learned that the bulk of the Watch's fighting force has been wiped out in the fight at the Fist…" (from node prose, wiki-sourced)

The cleanest single verbatim book line is asos-jon-06.md:51: "Feints. Mance wants us to spread ourselves thin, don't you see? And Bowen Marsh has obliged him. The gate is here. The attack is here." This explains the strategic situation but doesn't name the Fist specifically. For the edge, use the node-prose quote as tier-2 wiki-sourced or use the fight-at-the-fist node's own Quotes block (Mance/Jon exchange) as corroboration.

**D5 (rejected) — jon-spares-ygritte → jon-refuses-to-kill MOTIVATES**: The moral through-line (sparing Ygritte planted a bond that makes Jon refuse to kill an innocent) is narratively plausible but the text does not invoke it as the causal mechanism. Jon's refusal in asos-jon-05 is characterized as his Night's Watch conscience reasserting ("I won't murder an innocent man"), not as Ygritte-loyalty specifically. Keep as a NOTE; do not propose.

**Garrison-march-out node (lens-A dependency)**: The causal step between fight-at-the-fist and attack-on-castle-black SHOULD include a Bowen Marsh march-out event node (Mance sends raids → Bowen marches garrison north → Castle Black left with forty). The attack-on-castle-black Origins prose documents this chain. No such node exists. Lens A should build: `mance-rayder-sends-feint-raids` (or `bowen-marsh-marches-garrison-from-castle-black`) as an intermediate node; then fight-at-the-fist ENABLES that, and THAT ENABLES attack-on-castle-black. Without the intermediate node, D1 is the best available seam.

**jon-spares-ygritte and attack-on-the-wildlings (ACOK Skirling islands)**: As the baseline notes, these belong to the great-ranging arc. A potential seam: `jon-spares-ygritte ENABLES jon-refuses-to-kill` (ACOK mercy → ASOS refusal) might be worth flagging to the Skirling/Queenscrown lens but is out of this dip's scope.

**fight-at-the-fist duplicate**: Two nodes exist — `fight-at-the-fist` and `battle-of-the-fist-of-the-first-men`. Not investigated here (out of scope per brief). Flag for dedup pass.

**D6 upgrade caveat**: The `attack-on-castle-black CAUSES battle-beneath-the-wall` edge with quote "They must take the gate, or they cannot pass" is mechanically sound but the quote explains a precondition, not causation proper. ENABLES might be semantically cleaner (southern assault is a precondition enabling the northern one), but since the battle-beneath-the-wall was Mance's main assault — not a consequence of the southern assault failing — CAUSES is also defensible (the southern assault failing and confirming the Watch's tenacity triggered Mance committing his main host). Accept tier-2 upgrade; leave as CAUSES per existing edge type.

---

## HARVEST

- asos-jon-07.md:74-81 — food/meal: Owen delivers buns (warm, with raisins, pine nuts, dried apple), cheese, onions to the King's Tower sentries before the assault — "last meal" register; Jon: "There's no knowing when you'll have another chance."
- asos-jon-07.md:101 — food: "A loaf of black bread and a pail of Hobb's best mutton, cooked in a thick broth of ale and onions." Pre-battle meal; Jon notes "They ate every bit of it, using chunks of bread to wipe the bottom of the pail."
- asos-jon-08.md:25 — food/grim register: Clydas brings cups of hot mulled wine; Hobb passes black bread while men wait for the cage — siege-watch rations.
- asos-jon-08.md:85 — food/grim register: "Hobb rode up the chain with cups of onion broth, and Owen and Clydas served them to the archers where they stood, so they could gulp them down between arrows." — feeding men at their posts mid-battle.
- asos-jon-09.md:51 — food: Jon makes himself eat before the turtle assault: "bread, bacon, onions, and cheese" — "this might be my last meal" register.
- asos-jon-07.md:189-205 — iconic quote: Ygritte's death scene — "You know nothing, Jon Snow," she sighed, dying. Full verbatim death dialogue (asos-jon-07.md:193-205). High-value quote for node.
- asos-jon-08.md:171 — description: Noye locked in the giant's arms "looked almost like a child" — load-bearing physical description for Noye + Mag mutual-kill scene.
- asos-jon-08.md:47 — description: mammoths, giants on Wall assault — "a hundred" mammoths, giant roaring in Old Tongue, burning pitch barrels; vivid siege-warfare description.
- asos-jon-10.md:77-87 — food: Tormund and Jon share potent mead on the walk to Mance's camp — "a mead so potent that it made Jon's eyes water"; toasts to Donal Noye and Mag the Mighty; to Ygritte "kissed by fire." Hospitality-under-truce register, strong character beats.
- asos-jon-06.md:19 — grim register/Mole's Town: three-quarters of the village fled to Castle Black; brothel described ("a shed no bigger than a privy, its red lantern creaking in the wind"). Refugee hospitality.
