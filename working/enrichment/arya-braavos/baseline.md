# Baseline — Arya / Braavos (A2.3, build+enrich) — Session 150

> The SECOND-to-last A2 arc. **Build+enrich** (no spine exists). Identity-dissolution arc; ranked
> "architecturally isolated — low cross-arc payoff" (S143 plan). The dip's job: BUILD the Braavos
> event-spine + the identity-assumption nodes, wire the few genuine cross-arc seams, deepen the
> descriptive/object layer. **Mercy (TWOW preview) is forward-dangling → DEFER, do not mint.**

## Corpus — the 5 published Braavos-arc chapters (+ the ASOS departure)
- `sources/chapters/asos/asos-arya-13.md` — DEPARTURE. Boards the *Titan's Daughter*, pays the captain
  (Ternesio Terys), then gives the **iron coin** + says **"Valar morghulis"** (lines 231–259). Leaves Sandor off her list (:187).
- `sources/chapters/affc/affc-arya-01.md` — ARRIVAL. Passes the Titan; Yorko rows her in; the weirwood
  doors; the kindly man's **skull test** ("Kiss me, child"); she cycles Salty→Squab→Nan/Weasel→Arry→Arya Stark.
- `sources/chapters/affc/affc-arya-02.md` — NOVICE. "Who are you?"→"No one"; throws her Westeros things in
  the canal but **HIDES NEEDLE** behind a loose step; the Faceless-Men origin story; lie-detection training; becomes a novice.
- `sources/chapters/affc/affc-cat-of-the-canals-01.md` — CAT OF THE CANALS. Sells Brusco's oysters; hears
  **"Lady Lysa is dead, murdered by her own singer"** (:7, Vale-seam); **KILLS DAREON** the deserter in an
  alley (:15, "Just so"); reports it; the kindly man gives her the **warm milk → BLINDING**.
- `sources/chapters/adwd/adwd-the-blind-girl-01.md` — BLIND BETH. Trains blind; **wargs the one-eared cat**;
  the waif beats her with a stick; overhears Hardhome-slaves news (North-seam); catches the kindly man → **sight restored**.
- `sources/chapters/adwd/adwd-the-ugly-little-girl-01.md` — FIRST KILL FOR THE GOD. Assigned to kill the
  **insurance underwriter** (the "old man" at Purple Harbor); the **coin-swap** assassination; given the ugly
  dead girl's face; the wall of faces; her **face restored to Arya**; sent to Izembaro.

## Existing nodes (DO NOT re-mint)
- Characters: `arya-stark` (153 out-edges, saturated), `jaqen-hghar`, `kindly-man`, `waif`, `dareon`,
  `brusco`, `big-brusco`, `talea`, `brea`, `denyo-terys`, `ternesio-terys`, `umma`, `izembaro`, `lanna`,
  `blushing-bethany`, `samwell-tarly`, `gilly`, `sandor-clegane`, `syrio-forel`, `nymeria`, `rafford`, `tycho-nestoris`.
- Places: `braavos`, `titan-of-braavos` (ORPHAN, 0 edges), `house-of-black-and-white` (mis-typed as
  organization.house), `iron-bank-of-braavos`, `black-canal`/`green-canal`/`long-canal`/`canal-of-heroes`,
  `temple-of-the-lord-of-light-braavos`, `harrenhal`, `saltpans`.
- Factions/concepts: `faceless-men`, `many-faced-god`, `nights-watch`, `valar-morghulis`, `needle` (ORPHAN, 2 in-edges).
- Events: `kill-list-recitation-before-sleep`, `arya-captured`, `arya-frees-the-prisoners`, the Harrenhal
  three-deaths cluster (`chiswyck-dies-three-days-later`, `guards-killed`, `encounter-with-the-three-prisoners`).
- MISSING (mint targets): `merry`, `happy-port`, `iron-coin`, `salty`, `cat-of-the-canals`, `blind-beth`,
  any Braavos-arc EVENT node (arrival/identity/killing/blinding/sight/assassination), the insurance underwriter.

## Existing edges within the core node-set (70 unique — the dedup pull; DON'T re-mint these)
Key already-wired (sample): `arya KILLS dareon` (T1, adwd-blind-girl:141 — the reflection; the ACT is at
affc-cat-of-the-canals:15) · `arya WARGS_INTO nymeria` (T1, adwd-blind-girl) · `arya GUEST_OF kindly-man` ·
`arya GUEST_OF ternesio-terys` · `arya COMPANION_OF denyo-terys` · `arya SERVES brusco` (adwd-ugly-little-girl) ·
`arya SERVES umma` · `arya SEEKS kindly-man`/`jaqen` · `arya SWORN_TO faceless-men` (T2 wiki) ·
`kindly-man CLERGY_OF house-of-black-and-white` · `kindly-man TEACHES arya` · `jaqen TEACHES arya` (the coin) ·
`jaqen VOWS_TO arya` · `dareon BETRAYS nights-watch` · `dareon COURTS lanna` · `dareon OPPOSES samwell-tarly` ·
`dareon LOVER_OF blushing-bethany` · `dareon HATES gilly` · `ternesio PARENT_OF denyo`.
⚠ POSSIBLE DIRECTION ERROR (flag, don't fix unless clean): `arya-stark TUTORS kindly-man` (reversed — should be
kindly-man tutors Arya; `kindly-man TEACHES arya` already exists). Note for finalize.

## THE GAP (build targets)
**Spine event nodes (none exist):** sail-for-Braavos → arrival/skull-test → becomes-Cat-of-the-Canals →
killing-of-Dareon → blinding → blind-girl-training/sight-restored → ugly-little-girl-assassination/earns-a-face.
**Identity-dissolution nodes:** Cat of the Canals (event.deception, parallel to `sansa-adopts-the-alayne-stone-identity`),
"no one"/Blind Beth, the dead-girl face. **Object/place wiring:** `iron-coin` (precondition artifact, Jaqen's gift),
`needle` (the identity-retention anchor she HIDES), `titan-of-braavos`/`braavos` (Arya LOCATED_AT — she has NO presence edge!),
`house-of-black-and-white` LOCATED_AT.

## Cross-arc SEAMS (lens-4 priority — this "isolated" arc has a few genuine ones)
1. **Iron coin / Harrenhal → Braavos (STRONG):** the ACOK three-deaths (`jaqen TEACHES arya` the coin)
   ENABLES `arya-sails-for-braavos`. Wires the Harrenhal cluster FORWARD into Braavos.
2. **Dareon → Sam / Night's Watch / Oldtown (STRONG):** Dareon deserted (abandoned Sam + Aemon in Braavos;
   `dareon OPPOSES sam`, `dareon BETRAYS nights-watch`). Arya executes him as a deserter (Ned's justice). The
   killing connects Braavos ↔ the AFFC Sam/Oldtown arc (Dareon was their coin; his death strands Sam).
3. **Lysa-death news (Vale → Braavos, ECHO):** Cat hears "Lady Lysa is dead, murdered by her own singer"
   (cat-of-the-canals:7) — touches S148 `death-of-lysa-arryn`/`marillion`. Dramatic irony, both sisters cross
   unknowingly. Likely a HARVEST quote or weak REVEALS-style edge, not strong causal — lens-4 to assess.
4. **Hardhome slaves (North → Braavos, ECHO):** Blind Beth overhears wildling slaves from Hardhome sold in
   Braavos (blind-girl:15) — touches S145 `hardhome-catastrophe`. Harvest/weak.
5. **Kill-list tension:** the `kill-list-recitation-before-sleep` node is in tension with "no one" — she keeps
   reciting it. MOTIVATES her resistance to identity-dissolution.

## Run params
- run_id: `arya-braavos-enrichment-s150`. Backup edges before mint. NO container tag (Braavos/Vale not one of
  the 5 approved: essos/wo5k/north/aegon/bran). Theory-gated: Faceless-Men cosmology, the "valar morghulis"
  prophecy-reading, Mercy/Raff (TWOW) — evidence edges only, no theory assertions.
