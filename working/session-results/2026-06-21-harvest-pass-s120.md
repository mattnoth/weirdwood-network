# S120 Harvest-Consume Pass — Session Results
**Date:** 2026-06-21  
**Scope:** harvest-queue.md rows 219–271 (53 rows, all `open` at session start)  
**Model:** Sonnet

---

## Counts

| Action | Count |
|--------|-------|
| Attached (new content on node) | 37 |
| No-op / DEDUP (already present) | 15 |
| Parked (blocked, no home node) | 1 |
| **Total processed** | **53** |

---

## Edge Candidates (for orchestrator — not minted this pass)

| Candidate | Evidence | Source |
|-----------|----------|--------|
| Jorah Mormont WITNESS_IN drogo-blood-magic-ritual | Jorah finds blood-soaked footprints, reacts to ritual aftermath | `agot-daenerys-08.md:225` |
| Mossador BROTHER_OF Missandei | Named in nine-killed Sons-of-Harpy night | `adwd-daenerys-02.md:35` |
| Strong Belwas WITNESS_IN drogon-returns-to-daznak-pit | Falls to knees moaning as Drogon descends | `adwd-daenerys-09.md:233` |
| Ser Barristan Selmy WITNESS_IN drogon-returns-to-daznak-pit | "Look away, Your Grace" — present throughout pit chaos | `adwd-daenerys-09.md:233` |
| Reznak WITNESS_IN drogon-returns-to-daznak-pit | "He's eating her!" — named witness | `adwd-daenerys-09.md:233` |

---

## Cite-Drift Corrections (3 queue errors corrected at attach time)

| Row | Queue cite | Actual line | Note |
|-----|-----------|-------------|------|
| 249 | `asos-daenerys-04.md:44` | `:27` | Jorah's "Astapor was complacent and vulnerable" |
| 253 | `asos-daenerys-06.md:309` | `:325` | "Stay. Rule. And be a queen." |
| 259 | `adwd-daenerys-05.md:313` | `:307` | "I cannot fight two enemies" |

---

## Full Row Table

| Row | Cite | Kind | Home Node | Action | Note |
|-----|------|------|-----------|--------|------|
| 219 | agot-daenerys-06.md:179 | quote | drogo-westward-vow | no-op | already in ## Quotes at :179 |
| 220 | agot-eddard-08.md:13 | quote | robert-orders-daenerys-assassination | no-op | already in ## Quotes at :13 |
| 221 | agot-daenerys-09.md:127 | quote | drogo-blood-magic-ritual | no-op | base :127 quote already present; new quotes on same node from other rows |
| 222 | agot-daenerys-10.md:117 | foreshadowing | dragon-hatching-on-drogo-pyre | no-op | already in ## Quotes at :117; also in daenerys-targaryen as wiki-cite |
| 223 | agot-daenerys-10.md:121 | quote | dragon-hatching-on-drogo-pyre | no-op | already in ## Quotes at :121 |
| 224 | agot-daenerys-06.md:153 | foreshadowing | drogo-westward-vow | no-op | already in ## Quotes at :153 |
| 225 | agot-daenerys-09.md:163 | appearance | death-of-khal-drogo | no-op | already in ## Quotes at :163 (dedup list) |
| 226 | affc-the-princess-in-the-tower-01.md:325 | quote | doran-reveals-fire-and-blood-pact | no-op | already in ## Quotes at :325 (dedup list) |
| 227 | adwd-daenerys-09.md:103 | place | daznaks-pit | **attached** | book-cite overlay on ## Appearances & Description |
| 228 | adwd-daenerys-09.md:55 | quote | dany-mounts-drogon-and-flees-meereen | no-op | cite is wrong chapter; actual is adwd-10:55; already in dany-lost-on-dothraki-sea (dedup list) |
| 229 | adwd-daenerys-10.md:49 | quote | drogo-blood-magic-ritual | **attached** | retrospective cite overlay added to ## Quotes |
| 230 | agot-arya-03.md:73 | witness | (no node) | **parked** | No Varys-Illyrio conspiracy event node exists; WITNESS_IN edge candidate flagged |
| 231 | adwd-daenerys-09.md:109 | food | daznaks-pit | **attached** | concessions (dog sausages etc) added to ## Quotes |
| 232 | adwd-daenerys-09.md:233 | appearance | drogon-returns-to-daznak-pit | no-op | already in ## Quotes at :233 (dedup list) |
| 233 | agot-daenerys-06.md:71 | food | western-market | **attached** | horsemeat sausage / Pentoshi vendor added to ## Quotes |
| 234 | agot-daenerys-06.md:83 | food | western-market | **attached** | wine merchant's named-wine pitch added to ## Quotes |
| 235 | agot-daenerys-06.md:83 | appearance | the-wine-merchant-attempts-to-poison-dany | **attached** | Lysene appearance description added to ## Appearances & Description |
| 236 | agot-daenerys-06.md:51 | place | western-market | **attached** | square layout description added to ## Appearances & Description |
| 237 | agot-daenerys-07.md:85 | appearance | drogo | **attached** | battle wounds overlay added to ## Appearances & Description |
| 238 | agot-daenerys-07.md:133 | appearance | mirri-maz-duur | **attached** | first-appearance robes description added to ## Appearances & Description |
| 239 | agot-daenerys-09.md:115 | quote | drogo-blood-magic-ritual | **attached** | Rhaego stillbirth description added to ## Quotes |
| 240 | agot-daenerys-09.md:127 | quote | drogo-blood-magic-ritual | **attached** | Mirri's revenge motive dialogue added to ## Quotes |
| 241 | agot-daenerys-09.md:179 | foreshadowing | drogo-blood-magic-ritual | **attached** | Mirri's impossible-condition curse added to ## Quotes |
| 242 | agot-daenerys-08.md:225 | witness | drogo-blood-magic-ritual | **attached** | Jorah's reaction added to ## Quotes with WITNESS_IN edge candidate note |
| 243 | agot-daenerys-10.md:121 | appearance | dragon-hatching-on-drogo-pyre | no-op | same as row 223 — already in ## Quotes at :121 |
| 244 | asos-daenerys-03.md:15 | appearance | fall-of-astapor | **attached** | Qartheen gown appearance added to ## Quotes |
| 245 | asos-daenerys-03.md:15 | food | fall-of-astapor | **attached** | persimmon wine added to ## Quotes (same passage as row 244) |
| 246 | asos-daenerys-04.md:227 | food | fall-of-astapor | **attached** | trade goods inventory (saffron, maggot-olives, etc.) added to ## Quotes |
| 247 | asos-daenerys-04.md:139 | food | battle-near-yunkai | **attached** | Mero wine bribe appended to ## Quotes |
| 248 | asos-daenerys-03.md:253 | quote | fall-of-astapor | **attached** | "Dracarys." added to ## Quotes |
| 249 | asos-daenerys-04.md:44 → :27 | quote | fall-of-astapor | **attached** | Jorah's "Astapor complacent / Yunkai forewarned" added; cite corrected from :44 to :27 |
| 250 | asos-daenerys-05.md:11 | place | meereen | **attached** | book-cite overlay on ## Appearances & Description |
| 251 | asos-daenerys-05.md:33 | quote | siege-of-meereen | **attached** | 163-children vow added to ## Quotes |
| 252 | asos-daenerys-06.md:27 | quote | siege-of-meereen | **attached** | "sewer rats and a wooden cock" added to ## Quotes |
| 253 | asos-daenerys-06.md:309 → :325 | quote | siege-of-meereen | **attached** | "Stay. Rule. And be a queen." added; cite corrected from :309 to :325 |
| 254 | asos-daenerys-06.md:283 | food | siege-of-meereen | **attached** | Dany's first meal (lamb, raisins, honey bread) added to ## Quotes |
| 255 | adwd-daenerys-02.md:23 | quote | sons-of-the-harpy-kill-twenty-nine | **attached** | nine-killed scene opener added to ## Quotes |
| 256 | adwd-daenerys-02.md:35 | relationship | sons-of-the-harpy-kill-twenty-nine | **attached** | Mossador=Missandei's brother added to ## Quotes; BROTHER_OF edge candidate flagged |
| 257 | adwd-daenerys-02.md:107 | foreshadowing | daenerys-targaryen | **attached** | governing dilemma quote added to ### Quotes by Daenerys — ADWD |
| 258 | adwd-daenerys-04.md:67 | quote | wedding-of-hizdahr-zo-loraq-and-daenerys-targaryen | **attached** | "if a husband could help end the slaughter" appended to ## Quotes |
| 259 | adwd-daenerys-05.md:313 → :307 | quote | daenerys-targaryen | **attached** | "I cannot fight two enemies" added; cite corrected from :313 to :307 |
| 260 | adwd-daenerys-09.md:109 | food | daznaks-pit | **attached** | royal box provisions (honeyed locusts etc.) added to ## Quotes (combined with row 231) |
| 261 | adwd-daenerys-09.md:187 | appearance | barsena-blackhair | **attached** | canonical description added to ## Appearances & Description |
| 262 | adwd-daenerys-09.md:257 | quote | drogon-returns-to-daznak-pit | **attached** | "looking into hell" added; upgrades wiki-cite-only quote on drogon.node |
| 263 | adwd-daenerys-10.md:35 | appearance | dany-lost-on-dothraki-sea | **attached** | post-flight ragged appearance added to ## Appearances & Description |
| 264 | adwd-daenerys-10.md:199 | quote | dany-lost-on-dothraki-sea | **attached** | "Fire and Blood" to the grass added to ## Quotes |
| 265 | adwd-daenerys-10.md:89-95 | foreshadowing | dany-lost-on-dothraki-sea | **attached** | Quaithe vision added to ## Foreshadowing |
| 266 | adwd-daenerys-09.md:233 | witness | drogon-returns-to-daznak-pit | no-op | :233 already in ## Quotes; Belwas/Barristan/Reznak = edge candidates flagged |
| 267 | affc-the-princess-in-the-tower-01.md:47 | food | arianne-martell | no-op | already in ## Narrative Arc (S118, row 211) |
| 268 | affc-the-princess-in-the-tower-01.md:133 | appearance | arianne-martell | **attached** | ivory gown submission scene added to ## Appearances & Description |
| 269 | adwd-the-queens-hand-01.md:39 | appearance | death-of-quentyn-martell | no-op | already in ## Quotes at :39 (dedup list) |
| 270 | adwd-the-dragontamer-01.md:199 | quote | death-of-quentyn-martell | **attached** | "fire and blood, blood and fire" whisper added to ## Quotes |
| 271 | adwd-the-dragontamer-01.md:77 | foreshadowing | death-of-quentyn-martell | **attached** | Gerris dark joke added to ## Foreshadowing |

---

## Notable Book-Cite Overlays

These rows upgraded wiki-sourced descriptions (Tier-2 non-navigable cite_refs) to Tier-1 navigable book provenance:

- **western-market** — entire node rebuilt from stub: `## Appearances & Description` + `## Quotes` (rows 233–236)
- **drogo** — wounds paragraph (`agot-daenerys-07.md:85`) before existing wiki feasting-hall prose (row 237)
- **mirri-maz-duur** — first-appearance robe description overlaid on wiki description (row 238)
- **meereen** — first-sight description (`asos-daenerys-05.md:11`) overlaid before existing wiki Location section (row 250)
- **daznaks-pit** — entrance arch description (`adwd-daenerys-09.md:103`) added before wiki text (row 227)
- **barsena-blackhair** — canonical panther-grace first appearance added (row 261)
- **arianne-martell** — ivory submission gown added to existing wiki-sourced appearance block (row 268)
- **drogon-returns-to-daznak-pit** — "looking into hell" quote (`adwd-daenerys-09.md:257`) upgraded from wiki-only to book cite (row 262)

---

## Parked Row (1)

| Row | Reason |
|-----|--------|
| 230 | No Varys-Illyrio conspiracy event node exists. Arya WITNESS_IN edge candidate flagged. Unblock by minting a Varys-Illyrio conspiracy meeting event node. |

