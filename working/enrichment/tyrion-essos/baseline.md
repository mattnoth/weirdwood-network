# Baseline — A2.4 Tyrion / Essos enrichment (S161)

**The dedup ground-truth.** Generated from `baseline_pull.py` (180 internal edges, 16 causal). Every
node/edge a lens proposes MUST be deduped against this. This is a **BUILD + ENRICH with a HEAVY dedup** —
Tyrion is a saturated POV (224 core-out edges) and the Shy-Maid household + Meereen destination were
already built by **S147 (AEGON)** and **S144 (Daenerys/Meereen)**. **Aim proposals at the GAPS below.**

## The arc (ADWD Tyrion I–XII)
Tyrion's journey from Tywin's murder to the gates of Meereen: drinks across the narrow sea to **Pentos**
and **Illyrio**'s manse → boards the **Shy Maid** down the **Rhoyne** with Young Griff / Jon Connington
(Griff) / Haldon / Lemore / Duck / Yandry / Ysilla → the **Sorrows**, the **stone men** of the Bridge of
Dream, the greyscale scare, Tyrion pulled from the river (Jon Connington is the one infected) → slips off
at **Selhorys**, taken in a brothel → **captured by Jorah Mormont** (who means to bring him to Daenerys) →
**Volantis**, the widow of the waterfront, boards the cog **Selaesori Qhoran** with **Moqorro** and the
dwarf **Penny** (her brother **Oppo** was beheaded in Volantis) → shipwreck → **captured by slavers**, sold
to **Yezzan zo Qaggaz**, the dwarf-show in the Yunkish siege camp → the **pale mare** (bloody flux) sweeps
the camp, kills Yezzan → in the chaos Tyrion + Penny + Jorah flee and **join the Second Sons** at the
Meereen siege lines.

## Chapter map (which lens reads what — every chapter covered)
| ch | beat | lenses |
|----|------|--------|
| adwd-tyrion-01 | Pentos arrival, Illyrio's manse, the murder aftermath | A, B, D |
| adwd-tyrion-02 | Illyrio (the cheesemonger's game), departure | A, B |
| adwd-tyrion-03 | boards the Shy Maid, the household, cyvasse begins | B, C |
| adwd-tyrion-04 | the river, Young Griff, cyvasse, Selhorys approach | C |
| adwd-tyrion-05 | the Sorrows, the stone men, Bridge of Dream, greyscale, pulled from river | C, D |
| adwd-tyrion-06 | Selhorys, the brothel, slips away | B |
| adwd-tyrion-07 | **Jorah captures Tyrion** at the brothel; the cog | B |
| adwd-tyrion-08 | Volantis, the widow of the waterfront, Moqorro, Penny appears | A, B |
| adwd-tyrion-09 | aboard the Selaesori Qhoran, Moqorro, Penny | A, C |
| adwd-tyrion-10 | the becalmed ship, the dwarfs, Penny, red priest | C |
| adwd-tyrion-11 | **shipwreck → captured by slavers → sold to Yezzan**; pale mare begins | A, C |
| adwd-tyrion-12 | the dwarf-show, the **pale mare** kills Yezzan, **join the Second Sons**, Meereen | A, D |

## GAPS — aim here (the value of this dip)
**Causally ISLANDED event hubs (built but 0 causal edges):**
- `stone-men-attack-the-shy-maid` — cOut=0 cIn=0 (built S147). Tyrion + Aegon + Duck + Ysilla VICTIM_IN
  already. **ENRICH:** wire causal in (the river-voyage approach) + out (the greyscale seam — Jon Connington
  is infected pulling Tyrion from the river: `jon-connington AFFLICTED_BY greyscale` already exists; the
  attack is *where* he caught it). Tyrion-pulled-from-the-river beat.
- `trial-of-tyrion-lannister` — cOut=0 (15 in-roles, no causal). The launch web.
- `ben-plumm-defects-to-yunkai`, `wedding-of-hizdahr…`, `second-siege-of-meereen`, `arstan-kills-mero`,
  `battle-of-yunkai` (0 edges) — islanded; mostly NOT this arc's job (Dany-side), leave unless a clean seam.

**Beats with NO event node (exist only as dyad edges — BUILD candidates):**
- **Pentos arrival** — `illyrio PROTECTS/SEEKS tyrion`, `tyrion GUEST_OF illyrio` exist; no entry event.
  Mint to wire the launch FORWARD: `varys-smuggles-tyrion-out-of-kings-landing` is cOut=0 (islanded forward).
- **The Jorah capture** — `jorah-mormont CAPTURES tyrion-lannister` is a bare dyad; NO event node. BUILD.
- **The slaver capture / sale to Yezzan** — `tyrion KILLS nurse`, `yezzan-zo-qaggaz`/`sweets`/`nurse` nodes
  exist but NO capture/sale event. Penny is a major dyad (LOVES/COMPANION_OF/MOURNS-oppo). BUILD.
- **The pale mare / bloody flux** — `bloody-flux` node exists with **0 edges**. Light it (the flux kills
  Yezzan → enables the escape).
- **Tyrion joins the Second Sons** — `tyrion/penny/jorah MEMBER_OF + SWORN_TO second-sons` are bare dyads;
  `second-sons` cOut=1. NO joining event. BUILD the **terminus** → wire into `siege-of-meereen`.

## DEDUP HOT ZONES — do NOT re-mint (these are LIVE)
- **S147 AEGON/Golden Company:** the whole Shy-Maid household (`shy-maid`, `haldon`, `lemore`, `duck`,
  `rolly-duckfield`, `yandry`, `ysilla`, `jon-connington`, `aegon-targaryen-young-griff`, `illyrio-mopatis`,
  `illyrios-ruby-chain`), `stone-men-attack-the-shy-maid`, `exile-of-jon-connington`,
  `aegon-revealed-to-the-golden-company`, `golden-company-sails-for-westeros`, `jon-connington AFFLICTED_BY
  greyscale`, `greyscale MOTIVATES jon-connington`, `tyrion MANIPULATES aegon`. The fAegon-reveal / cyvasse-
  with-Aegon dyads exist. **Pull only Tyrion-side beats S147 left islanded.**
- **S144 Daenerys/Meereen:** `siege-of-meereen`, `second-siege-of-meereen`, `battle-near-yunkai`,
  `fall-of-astapor`, `ben-plumm-defects-to-yunkai` (the THIRD treason — Dany-side, Ben leaving Dany),
  `wedding-of-hizdahr…`, the sons-of-the-harpy web, `ben-plumm BETRAYS/SERVES/COMMANDS daenerys`,
  `jorah BETRAYS/LOVES/SERVES daenerys`, `daenerys BANISHES/SEEKS/MOURNS jorah`. **Do NOT touch the
  Dany-side Meereen spine** — only wire Tyrion's terminus INTO `siege-of-meereen`.
- **S109/S139 Tywin's-death:** `assassination-of-tywin-lannister`, `tyrion-kills-shae-in-tywins-bed`,
  `trial-of-tyrion-lannister`, `jaime-frees-tyrion-from-the-black-cells`, `jaime-reveals-the-truth-of-tysha`,
  `varys-smuggles-tyrion-out-of-kings-landing` (the launch), `tyrion AGENT_IN` those. **Wire FORWARD only**
  (smuggling → Pentos), do NOT re-mint the KL web.
- **The dense Tyrion/Illyrio/Varys/JonCon/Jorah/Penny dyad web** (180 internal edges) — the dedup WILL kill
  many proposals. Do not re-propose existing dyads.

## DO NOT
- **No TWOW.** The Second-Sons-turn-their-cloaks-BACK-to-Daenerys happens in *The Winds of Winter* — in
  **ADWD Tyrion only JOINS / sells himself into the Second Sons** and conceives the plan. Mint the JOINING
  (ADWD), keep the executed back-defection node-prose only. There is a `tyrion-ii-the-winds-of-winter` node —
  do NOT touch/extend it.
- **No theory assertions (GATED):** Aegon-is-real / fAegon, Illyrio's true parentage game, any prophecy /
  Moqorro-fire reading. Evidence/act/MOTIVATES→character edges only; readings stay node-prose.
- **Container:** `essos` IS one of the 5 approved containers. Genuine Essos-set beats TAKE `containers:
  [essos]` (Pentos/Rhoyne/Volantis/Selhorys/the slave camp/Meereen are all Essos). The lenses do NOT tag
  (synthesis decides); but unlike Jaime's Riverlands, here the tag IS warranted for the new nodes.
- No container outside the approved 5. No show-canon. Honor ENABLES-vs-CAUSES; route human choices through
  MOTIVATES(→character).
