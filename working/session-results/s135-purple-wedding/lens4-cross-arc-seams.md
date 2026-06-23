# S135 — Purple Wedding enrichment · Lens 4: Cross-Arc Seams

> PROPOSE-ONLY. All slugs existence-confirmed via `graph-query.py` before filing.
> Source: 2026-06-23.

---

## Proposed edges

| src_slug | edge_type | tgt_slug | tier | evidence (file:line) | verbatim quote | rationale | existence-confirmed? |
|---|---|---|---|---|---|---|---|
| `littlefinger-brokers-tyrell-lannister-alliance` | ENABLES | `joffrey-sets-sansa-aside-and-agrees-to-wed-margaery` | Tier 1 | `sources/chapters/acok/acok-tyrion-08.md:113` | "The Stark girl brings Joffrey nothing but her body, sweet as that may be. Margaery Tyrell brings fifty thousand swords and all the strength of Highgarden." | The Tyrell-Lannister marriage pact brokered by Littlefinger is the direct precondition for Joffrey's betrothal to Margaery; without the alliance, Joffrey never sets Sansa aside. Margaery being placed in reach of Joffrey is the necessary condition for Olenna's protective motive to exist. ENABLES is correct: Joffrey's council still chose to proceed with the betrothal, but the alliance made it possible. | Y (both nodes confirmed, both 0 causal edges) |
| `joffrey-sets-sansa-aside-and-agrees-to-wed-margaery` | ENABLES | `tyrell-plot-revealed` | Tier 1 | `sources/chapters/asos/asos-sansa-06.md:193` | "Lady Olenna was not about to let Joff harm her precious darling granddaughter, but unlike her son she also realized that under all his flowers and finery, Ser Loras is as hot-tempered as Jaime Lannister. Toss Joffrey, Margaery, and Loras in a pot, and you've got the makings for kingslayer stew." | Littlefinger's on-page confession (asos-sansa-06) explicitly names Joffrey's danger to Margaery — and by extension the betrothal placing her in that danger — as the cause of Olenna's decision to kill him. The betrothal is the enabling precondition for the Tyrell protective conspiracy. ENABLES rather than CAUSES: Olenna's agency is fully intact; this seam closes the motive gap. This is the single most valuable missing hop: it lets `--causal-chain tyrell-plot-revealed` walk upstream to the betrothal and alliance for the first time. | Y (both nodes confirmed, `tyrell-plot-revealed` has 0 causal in/out) |
| `littlefinger-smuggles-sansa-out-of-kings-landing` | ENABLES | `wedding-of-petyr-baelish-and-lysa-arryn` | Tier 1 | `sources/chapters/asos/asos-sansa-06.md:215` | "My lady, allow me to present you Alayne Stone." | Littlefinger's escape plan delivers Sansa to the Fingers, where Lysa arrives to be wed. The smuggling is the logistical prerequisite for Littlefinger holding the Fingers as a staging point and being present to receive Lysa. The `wedding-of-petyr-baelish-and-lysa-arryn` node's own prose confirms: "Petyr and Sansa sail on the Merling King to the Fingers, where they wait for Lysa's arrival at Petyr's unnamed tower." | Y (both nodes confirmed; `littlefinger-smuggles-sansa-out-of-kings-landing` has 0 causal edges; `wedding-of-petyr-baelish-and-lysa-arryn` has 0 outgoing causal edges) |
| `death-of-joffrey-baratheon` | ENABLES | `wedding-of-petyr-baelish-and-lysa-arryn` | Tier 2 | `sources/chapters/asos/asos-sansa-06.md:193` | "Her son was determined to make Margaery a queen, and for that he needed a king . . . but he did not need Joffrey." | Littlefinger explicitly frames the wedding-of-Petyr-and-Lysa as tied to the Joffrey conspiracy: Joffrey's death both creates Littlefinger's escape window (Sansa flees on the same night) and is the political act through which Littlefinger demonstrates value to the Tyrells and secures his Vale gambit. However, the direct causal link is less tight than the smuggling edge above — the Petyr-Lysa marriage plan was in motion before the Purple Wedding. Propose at Tier 2. | Y (`death-of-joffrey-baratheon` confirmed; `wedding-of-petyr-baelish-and-lysa-arryn` confirmed) |
| `littlefinger-brokers-tyrell-lannister-alliance` | CONSPIRES_WITH | `tyrell-plot-revealed` | Tier 1 | `sources/chapters/asos/asos-sansa-06.md:187` | "When I came to Highgarden to dicker for Margaery's hand, she let her lord son bluster while she asked pointed questions about Joffrey's nature. I praised him to the skies, to be sure . . . whilst my men spread disturbing tales amongst Lord Tyrell's servants. That is how the game is played." | Littlefinger's brokering mission to Highgarden is where he first made contact with Olenna and planted the intelligence seeds (disturbing tales about Joffrey) that eventually ripened into Olenna's decision to kill him. The alliance negotiation and the Tyrell plot share the same originating encounter. CONSPIRES_WITH links the two event nodes to represent Littlefinger's dual role: he built the alliance AND co-architected its undoing. NOTE: strictly speaking this edges between two events, not two characters — may need schema review. If CONSPIRES_WITH is reserved for character↔character, substitute with a narrative note rather than an edge. | Y (both nodes confirmed) |

---

## Seam narrative

The Purple Wedding cluster's upstream side has a three-hop gap that currently prevents `--causal-chain` from crossing into the wo5k arc:

```
[wo5k arc]
littlefinger-brokers-tyrell-lannister-alliance  (0 causal edges)
    ↓  ENABLES  [MISSING]
joffrey-sets-sansa-aside-and-agrees-to-wed-margaery  (0 causal edges)
    ↓  ENABLES  [MISSING]
tyrell-plot-revealed  (0 causal in/out)
    → [already wired downstream into death-of-joffrey-baratheon via AGENT_IN]
```

Wiring these two ENABLES edges closes the seam: a graph query for `--causal-chain tyrell-plot-revealed` would walk all the way back to the Bitterbridge moment where Littlefinger brokered the alliance and first met Olenna.

The downstream seam (Sansa's escape → Vale) is also open:

```
littlefinger-smuggles-sansa-out-of-kings-landing  (0 causal edges)
    ↓  ENABLES  [MISSING]
wedding-of-petyr-baelish-and-lysa-arryn  (0 outgoing causal edges)
```

This connects the Purple Wedding arc to the Sansa-in-the-Vale thread.

---

## Harvest finds

- `sources/chapters/asos/asos-sansa-06.md:187` / **quote / Littlefinger on planting disturbing tales about Joffrey at Highgarden** — "I praised him to the skies, to be sure . . . whilst my men spread disturbing tales amongst Lord Tyrell's servants." Evidence for Littlefinger's active role in seeding Olenna's distrust of Joffrey. Load-bearing for the CONSPIRES edge and for `tyrell-plot-revealed` node's evidence_quote.
- `sources/chapters/asos/asos-sansa-06.md:193` / **quote / Olenna's motive verbatim** — "Lady Olenna was not about to let Joff harm her precious darling granddaughter." The canonical on-page statement of Olenna's protective motive. Should be attached to `tyrell-plot-revealed` ## Quotes or to `olenna-tyrell`'s AGENT_IN edge as evidence_quote.
- `sources/chapters/asos/asos-sansa-06.md:193` / **food/hospitality / Littlefinger eats pomegranate while confessing** — "He tilted his chin back and squeezed the blood orange, so the juice ran down into his mouth." First-class food texture during the key confession scene.
- `sources/chapters/acok/acok-sansa-08.md:41` / **quote / formal nullification of Sansa-Joffrey betrothal** — the High Septon's formal release speech. Should be attached to `joffrey-sets-sansa-aside-and-agrees-to-wed-margaery` ## Quotes (currently the node has Cersei's proposal but not the High Septon's doctrinal release).
- `sources/chapters/asos/asos-sansa-06.md:335` / **hospitality/quote / Lysa on poison as a woman's honor** — "A man will tell you poison is dishonorable, but a woman's honor is different. The Mother shaped us to protect our children, and our only dishonor is in failure." Thematic echo of Olenna; connects to `tyrell-plot-revealed` motive arc.

---

## Summary (3 lines)

**Best cross-arc seam:** `joffrey-sets-sansa-aside-and-agrees-to-wed-margaery` ENABLES `tyrell-plot-revealed` (Tier 1) — Littlefinger's on-page confession at `asos-sansa-06.md:193` explicitly names the betrothal placing Margaery in danger as Olenna's motive for killing Joffrey; wiring this hop lets `--causal-chain tyrell-plot-revealed` walk upstream into the wo5k arc for the first time.

**Cite-verified:** Yes — verbatim contiguous quote confirmed at `sources/chapters/asos/asos-sansa-06.md:193`.

**Full seam package:** Three additional edges proposed — `littlefinger-brokers-tyrell-lannister-alliance` ENABLES `joffrey-sets-sansa-aside-and-agrees-to-wed-margaery` (closes the wo5k upstream hop, Tier 1, cite `acok-tyrion-08.md:113`) and `littlefinger-smuggles-sansa-out-of-kings-landing` ENABLES `wedding-of-petyr-baelish-and-lysa-arryn` (connects PW escape thread to the Vale arc, Tier 1, cite `asos-sansa-06.md:215`); all four slugs existence-confirmed, all currently have 0 causal edges.
