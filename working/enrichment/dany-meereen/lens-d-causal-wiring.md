# Lens D — Causal Wiring: Daenerys / Meereen (Slaver's Bay)
Produced: 2026-06-24

---

## DEDUP NOTES (existing edges verified before proposing)

These seams are already wired — no re-proposal needed:

| Edge | Status |
|------|--------|
| `sons-of-the-harpy-kill-twenty-nine` CAUSES `wedding-of-hizdahr-zo-loraq-and-daenerys-targaryen` | EXISTS (ref: adwd-daenerys-04.md:283) |
| `galazza-counsels-the-ghiscari-marriage` CAUSES `wedding-of-hizdahr-zo-loraq-and-daenerys-targaryen` | EXISTS |
| `wedding-of-hizdahr-zo-loraq-and-daenerys-targaryen` ENABLES `drogon-returns-to-daznak-pit` | EXISTS (ref: adwd-daenerys-06.md:139) |
| `drogon-returns-to-daznak-pit` TRIGGERS `dany-mounts-drogon-and-flees-meereen` | EXISTS |
| `dany-mounts-drogon-and-flees-meereen` CAUSES `dany-lost-on-dothraki-sea` | EXISTS |
| `siege-of-meereen` CAUSES `sons-of-the-harpy-kill-twenty-nine` | EXISTS |
| `robert-orders-daenerys-assassination` CAUSES `the-wine-merchant-attempts-to-poison-dany` | EXISTS |
| `the-wine-merchant-attempts-to-poison-dany` CAUSES `drogo-westward-vow` | EXISTS |
| `quentyn-orders-the-attack` TRIGGERS `death-of-quentyn-martell` | EXISTS |
| `death-of-khal-drogo` CAUSES `dragon-hatching-on-drogo-pyre` | EXISTS |

**Orphaned nodes confirmed (zero edges outgoing/incoming):**
- `second-siege-of-meereen` — 0 edges total
- `dragon-hatching-on-drogo-pyre` — 0 outgoing
- `doran-reveals-fire-and-blood-pact` — 0 outgoing
- `death-of-quentyn-martell` — 0 outgoing
- `poisoned-locusts` — 0 edges total

---

## PROPOSED CAUSAL EDGES

### EDGE D-1
**`doran-reveals-fire-and-blood-pact` MOTIVATES `quentyn-orders-the-attack`**

- **tier:** 1
- **ref:** `sources/chapters/adwd/adwd-the-spurned-suitor-01.md:71`
- **quote:** `"This is what I have to do. For Dorne. For my father. For Cletus and Will and Maester Kedry."`
- **why proximate, not distal:** Quentyn explicitly states his father's commission as the operative motive in the moment of decision to steal a dragon. The pact is the specific obligation he is acting under. The intermediate step (Doran sent Quentyn to Essos to fulfill the pact) is already encoded in the pact node's description; this MOTIVATES names the pact as what compels the specific dangerous act. Not distal: Quentyn's stated reason is the duty his father laid on him, not some further-upstream cause.
- **supplementary quote (adwd-the-spurned-suitor-01.md:75):** `"All dead... For what? To bring me here, so I might wed the dragon queen. A grand adventure, Cletus called it... Their deaths should have some meaning."`
- **note:** `doran-reveals-fire-and-blood-pact` currently has 0 outgoing edges. This is its first downstream causal link.

---

### EDGE D-2
**`dany-mounts-drogon-and-flees-meereen` ENABLES `quentyn-orders-the-attack`**

- **tier:** 1
- **ref:** `sources/chapters/adwd/adwd-the-spurned-suitor-01.md:67`
- **quote:** `"'The dragon has three heads,' she said to me. 'My marriage need not be the end of all your hopes,' she said. 'I know why you are here. For fire and blood.' I have Targaryen blood in me, you know that."`
- **why proximate, not distal:** Quentyn's decision to steal a dragon is directly enabled by two simultaneous facts: Dany is wed to Hizdahr (foreclosing the marriage) AND Dany has now flown away on Drogon (leaving Rhaegal and Viserion unchained and unguarded). Both conditions must be true. The marriage-closed / queen-absent situation is what Quentyn cites when explaining why he must prove himself via dragonriding rather than by wedlock. Without Dany's flight, Rhaegal and Viserion remain under closer supervision — the flight is what opens the window. The Tattered Prince's dialogue at adwd-the-spurned-suitor-01:127 makes this explicit: "Your bride flew off on a dragon. Well, when she returns, do be sure to invite us to your nuptials."
- **supplementary ref:** `sources/chapters/adwd/adwd-the-spurned-suitor-01.md:127` — `"Your bride flew off on a dragon... Could that be true? Surely not. What of your marriage pact?"`
- **note on agency-collapse check:** The proximate causal chain is: Dany's flight → dragons less guarded → Quentyn's window opens. This edge names the enabling event. The motivating obligation (the pact) is D-1 above. Both are needed; neither alone suffices.

---

### EDGE D-3
**`sons-of-the-harpy-kill-twenty-nine` SUSPECTED_OF `poisoned-locusts`**

- **tier:** 2
- **ref:** `sources/chapters/adwd/adwd-the-queensguard-01.md:155`
- **quote:** `"Hizdahr's confectioner. His name would mean nothing to you. The man was just a catspaw. The Sons of the Harpy took his daughter and swore she would be returned unharmed once the queen was dead."`
- **why proximate, not distal:** The Sons of the Harpy are the identified (via informant) proximate actors who coerced the confectioner into placing the poison in the locust bowl. The confectioner is merely a tool. SUSPECTED_OF is correct because Hizdahr's guilt versus the Sons' direct chain remains contested in-text; Skahaz asserts the Sons, Hizdahr denies it.
- **note:** `poisoned-locusts` node exists at `graph/nodes/foods/poisoned-locusts.node.md` with 0 edges. This is its first causal link.

---

### EDGE D-4
**`dragon-hatching-on-drogo-pyre` ENABLES `fall-of-astapor`**

- **tier:** 1
- **ref:** `sources/chapters/asos/asos-daenerys-01.md:231`
- **quote:** `"An army," said Ser Jorah. "If Strong Belwas is so much to your liking you can buy hundreds more like him out of the fighting pits of Meereen . . . but it is Astapor I'd set my sails for. In Astapor you can buy Unsullied."`
- **supporting context ref:** `sources/chapters/asos/asos-daenerys-01.md:257` — `"Dragons will be as great a wonder in Astapor as they were in Qarth. It may be that the slavers will shower you with gifts, as the Qartheen did."` / and line 255: `"How am I to buy a thousand slave soldiers? All I have of value is the crown..."`
- **why proximate, not distal:** Without living dragons, Dany has no bargaining power in Astapor — Jorah explicitly says the dragon eggs / live dragons are what make the slavers take her seriously, and the fall of Astapor depends on her having the Unsullied, which she acquires using Drogon as the exchange good. The hatching is not merely a distant background condition; it is the specific asset that funds the Unsullied purchase that executes the fall. This edge does not skip steps: hatching → (Dany has dragons) → fall-of-astapor. There is no intermediate named event node between them in the graph.
- **note:** `dragon-hatching-on-drogo-pyre` has 0 outgoing edges. This is its first downstream causal link.

---

### EDGE D-5
**`dany-mounts-drogon-and-flees-meereen` CAUSES `second-siege-of-meereen`**

- **tier:** 2
- **ref:** `sources/chapters/adwd/adwd-the-queensguard-01.md:59`
- **quote:** `"He had dreamed of it again last night: Belwas on his knees retching up bile and blood, Hizdahr urging on the dragonslayers, men and women fleeing in terror, fighting on the steps, climbing over one another, screaming and shouting. And Daenerys …"`
- **supporting context ref:** `sources/chapters/adwd/adwd-the-queensguard-01.md:159` — Skahaz: `"That was before. The pit changed all. Daenerys gone, Yurkhaz dead. In place of one old lion, a pack of jackals."`
- **why proximate, not distal:** The Queensguard chapter (Barristan's POV) explicitly names "Daenerys gone" and "Yurkhaz dead" (who died in the Daznak panic) as the twin causes that collapse the peace and embolden the more aggressive Yunkish faction (Bloodbeard et al.) to resume the siege. Dany's flight is the proximate trigger that removes the deterrent (the queen + her dragon) and kills the old guard Yunkish negotiator simultaneously. The second siege does not begin until after the pit/flight. Tier-2 because the causal line is narrated through Skahaz (interpretive), not a direct authorial statement of consequence.
- **note:** `second-siege-of-meereen` has 0 edges total. This is its first causal link.

---

### EDGE D-6 (CROSS-CONTAINER: essos → aegon/dorne)
**`death-of-quentyn-martell` PREVENTS `doran-martell-targaryen-alliance`**

- **HOLD — no suitable existing target node found.** A node for the Dornish-Targaryen alliance outcome does not exist in `graph/nodes/`. The `doran-reveals-fire-and-blood-pact` node is the closest, but it names the *reveal* event, not the *fulfilled alliance*. **Lens B should check whether an "arianne-dorne-targaryen-alliance-planned" or equivalent event node was minted.** If so, PREVENTS is the correct edge (Quentyn's death eliminates the Dornish heir who was to seal the pact through marriage). **Deferred pending node existence check.**

---

## CROSS-CONTAINER SEAMS (called out separately)

### Seam 1: AGOT→Essos (dragon hatching → conquest, D-4 above)
The `dragon-hatching-on-drogo-pyre` node sits at the end of the AGOT container spine and has no forward links into the Essos arc. Edge D-4 above (`dragon-hatching-on-drogo-pyre` ENABLES `fall-of-astapor`) is the primary AGOT→Essos causal seam. Without it, the entire Slaver's Bay arc appears causally unrooted in the graph — it begins with `fall-of-astapor` and no one can trace why Dany has the power to take Astapor.

### Seam 2: Essos→Dorne/Aegon (Quentyn mission → dragon-taming attempt, D-1 + D-2)
`doran-reveals-fire-and-blood-pact` (aegon/dorne container) → `quentyn-orders-the-attack` (essos container). Currently the Dornish pact and the Quentyn dragon-taming plot exist as disconnected subgraphs. Edges D-1 (MOTIVATES) and D-2 (ENABLES) stitch them together at the correct proximate links.

### Seam 3: Essos→Essos internal (Dany's flight → second siege, D-5)
`dany-mounts-drogon-and-flees-meereen` (essos, end of ADWD proper) → `second-siege-of-meereen` (essos, TWOW territory). The spine currently ends at `dany-lost-on-dothraki-sea` with no causal path to the second siege. D-5 provides the missing link.

### Seam 4: AGOT→Essos — wine-merchant → dragon hatching (ALREADY WIRED)
`the-wine-merchant-attempts-to-poison-dany` → `drogo-westward-vow` → `drogo-blood-magic-ritual` → `death-of-khal-drogo` → `dragon-hatching-on-drogo-pyre`: this chain is correctly wired. The missing link is from `dragon-hatching-on-drogo-pyre` forward into the Essos arc (D-4 above).

---

## NEEDS_VOCAB

None. All proposed edges use locked vocabulary: CAUSES / ENABLES / MOTIVATES / SUSPECTED_OF / PREVENTS.

---

## HARVEST

Drops found while reading the source text (not extracted, just pointers):

- `sources/chapters/adwd/adwd-daenerys-09.md:109` — **food:** "Hizdahr had stocked their box with flagons of chilled wine and sweetwater, with figs, dates, melons, and pomegranates, with pecans and peppers and a big bowl of honeyed locusts." — Royal box provisions at Daznak, food register entry.
- `sources/chapters/adwd/adwd-daenerys-09.md:109` — **food:** peddlers in the pit selling "dog sausages, roast onions, and unborn puppies on a stick" — grim food register, fighting pit concession food.
- `sources/chapters/adwd/adwd-the-dragontamer-01.md:81` — **food:** Quentyn's last meal before the dragon-taming attempt: "a simple meal of fruit and bread and cheese, washed down with goat milk" — condemned-man's breakfast quality; thematic resonance.
- `sources/chapters/adwd/adwd-the-dragontamer-01.md:15` — **description / foreshadowing:** "he held his palm above the flame. It took every bit of will he had to lower it until the fire touched his flesh, and when it did he snatched his hand back with a cry of pain." — Quentyn tests himself against fire; foreshadows his death by dragonfire. Classic Chekhov's gun / foreshadowing entry.
- `sources/chapters/adwd/adwd-the-dragontamer-01.md:237` — **quote / character perception:** "He knows that she is female. He is looking for Daenerys. He wants his mother and does not understand why she's not here." — Quentyn reads Viserion's behavior; load-bearing observation about dragon cognition + Dany's absence as a factor in the attack.
- `sources/chapters/adwd/adwd-daenerys-06.md:139` — **quote (already evidenced in wedding→pit edge):** Reznak's line about fighting pits as "wedding gift to Hizdahr and to your loving people" — already wired; note for completeness.
- `sources/chapters/adwd/adwd-daenerys-07.md:307` — **quote:** "I want to plant my olive trees and see them fruit." — Dany's stated desire for peace on her wedding day; characterization anchor.
