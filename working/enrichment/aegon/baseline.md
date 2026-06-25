# AEGON / Golden Company — Enrichment Pass 1 Baseline (S147)

> **Dip:** AEGON enrichment (the LAST spine-only heavyweight; reopened L1 round, dip #4 of 4 after Dany S144 / Jon S145 / Bran S146).
> **Spine built S128** (build-phase map: `working/aegon-decomposition.md`). This is the **enrichment** pass — the off-spine substrate.
> **Read-only baseline.** Live graph verified via `graph-query.py --container/--full-chain/--neighbors` + `edges.jsonl` greps, 2026-06-25.
> Graph at **22,808 edges**, vocab **170** (locked: `working/wiki/data/edge-type-counts.md`).

## THEORY GATE (hard) — read before proposing anything
The AEGON arc is a theory minefield. **Assert NO theory readings.** GATED, evidence-edges only:
- **Aegon-is-a-Blackfyre / "mummer's dragon"** — do NOT mint a `SUSPECTED_OF` on Aegon's *identity*; do NOT assert he's fake. The on-page "is he real?" doubt may be captured as **harvest quotes**, never as a graph claim about identity.
- **fAegon babe-swap** (Varys/Elia's infant) — the two `aegon-targaryen-son-of-rhaegar` (murdered infant) vs `aegon-targaryen-young-griff` (claimant) nodes are an identity question = GATED. **All new edges target `aegon-targaryen-young-griff`.**
- R+L, Azor Ahai, Euron↔Bloodraven — GATED.
The whodunit lens here is the **Varys/assassinations** whodunit (on-page fact), NOT "is Aegon real."

## The locked vocab (verify membership EXACTLY before any emit)
170 canonical types. AEGON-relevant confirmed in-vocab: `CAUSES TRIGGERS ENABLES MOTIVATES PREVENTS SUSPECTED_OF` · `CONSPIRES_WITH CONTRACTED_WITH NEGOTIATES_WITH ALLIES_WITH OPPOSES MANIPULATES BETRAYS MEMBER_OF FOUNDED` · `AGENT_IN VICTIM_IN WITNESS_IN COMMANDS_IN FIGHTS_IN PARTICIPATES_IN BESIEGES CAPTURES KILLS ATTACKS GUARDS` · `AFFLICTED_BY DIED_OF HEALS` · `DECEIVES REVEALS_TO SPIES_ON INFORMS DISGUISED_AS IMPERSONATES SEEKS IGNORANT_OF` · `SUB_BEAT_OF PART_OF` · `WIELDED_IN OWNS WIELDS GIFTED_TO PURCHASED_FROM CAPTAIN_OF CREW_OF` · `LOCATED_AT TRAVELS_TO TRAVELS_WITH IMPRISONED_AT` · `FEARS TRUSTS DISTRUSTS PROTECTS COMPANION_OF RESPECTS PERCEIVED_AS REPUTED_AS ENCOUNTERS` · `DEPICTED_IN FORESHADOWS PARALLELS` · `NAMED_AFTER`. If a relationship doesn't fit, flag `NEEDS_VOCAB:` — do NOT invent a type.

---

## Current spine (built S128, LIVE) — `--full-chain landing-of-the-golden-company` = 17 edges
```
[upstream, cross-arc auto-join from the Purple Wedding chain]
 ... → jaime-reveals-the-truth-of-tysha MOTIVATES tyrion-lannister
       battle-of-the-bells CAUSES exile-of-jon-connington
       exile-of-jon-connington ENABLES(precond) aegon-revealed-to-the-golden-company
       varys MOTIVATES aegon-revealed-to-the-golden-company
       aegon-revealed-to-the-golden-company TRIGGERS golden-company-sails-for-westeros
       aegon-targaryen-young-griff MOTIVATES golden-company-sails-for-westeros
       tyrion-lannister MOTIVATES golden-company-sails-for-westeros
       golden-company-sails-for-westeros CAUSES landing-of-the-golden-company
[downstream]
       landing-of-the-golden-company CAUSES siege-of-storms-end-300
       landing-of-the-golden-company MOTIVATES assassinations-of-pycelle-and-kevan-lannister
```
Build-step-0 cleanup CONFIRMED done: the suspicious `landing PRECEDES wedding-of-hizdahr…` edge = GONE; the `landing/assassinations PART_OF war-of-the-five-kings` edge-bug = GONE.

## Per-node state (what's built → the dedup map)
| Node | type | container | out | in | enrichment gap |
|---|---|---|---|---|---|
| `landing-of-the-golden-company` | event.battle | [aegon] | 2 (CAUSES siege, MOTIVATES assass.) | 8 (CAUSES sails, GUARDS gorys, 6×PART_OF takings) | role edges on the landing itself thin; harry-strickland/aegon/jon-con AGENT_IN absent |
| `assassinations-of-pycelle-and-kevan-lannister` | event.battle | [aegon] | **0** | 4 (varys AGENT_IN, landing MOTIVATES, kevan+pycelle VICTIM_IN) | **0 outgoing** — the KL-endgame *collapse* attach is unwired (lens 4). NB `varys KILLS kevan`+`KILLS pycelle` already exist as dyads too |
| `siege-of-storms-end-300` | event.battle | [aegon,wo5k] | 1 (PART_OF wo5k) | 2 (landing CAUSES, jon-con MOTIVATES) | participant roles absent (aegon insists on leading; GC officers); the AFFC Tyrell-siege seam |
| `aegon-revealed-to-the-golden-company` | event.incident | [aegon] | 1 (TRIGGERS sails) | 2 (exile ENABLES, varys MOTIVATES) | the war-council audience (Strickland, GC officers) absent; jon-con AGENT_IN absent |
| `golden-company-sails-for-westeros` | event.incident | [aegon] | 1 (CAUSES landing) | 3 (aegon+tyrion MOTIVATES, reveal TRIGGERS) | the broken Volantis/Yunkai contract (CONTRACTED_WITH?) absent; harry-strickland reluctance |
| `stone-men-attack-the-shy-maid` | event.incident | **untagged?** | 1 (LOCATED_AT shy-maid) | 5 (stone-men AGENT_IN; ysilla/aegon/tyrion/duck VICTIM_IN) | the greyscale-vector seam (JonCon infected here? actually JonCon hides it earlier) — verify; haldon/lemore/duck roles; **needs `[aegon]` tag** (was untagged at decomp) |
| 6 takings (mistwood/tarth/crows-nest/greenstone/griffins-roost/rain-house) | event.battle | mostly untagged | PART_OF landing | thin | **need `[aegon]` retag**; commander roles (Tristan Rivers, Laswell Peake, Marq Mandrake, Connington) absent. griffins-roost has 4 SUB_BEAT_OF children already |

## Character webs (densities → dedup targets; ENRICH the arc, the web falls out)
- `aegon-targaryen-young-griff` — 28 (15 out / 13 in). aliases "Young Griff", "Aegon VI". **All new edges → this slug.**
- `jon-connington` — **65** (45/20). Already fairly dense (wiki). Greyscale, exile, Storm's-End decision.
- `varys` — **59** (38/21) — the C1 thin-major-player target. ALREADY built: `CONSPIRES_WITH illyrio-mopatis` (×2), `KILLS kevan/pycelle`, `AGENT_IN assassinations`, `MOTIVATES aegon-revealed`, `BETRAYS/DECEIVES ned`, `SPIES_ON tywin/catelyn`, antler-men, the smuggle-tyrion. Gap: the Aegon spy-network / little-birds / Rugen-identity / "for the realm" motive substrate.
- `illyrio-mopatis` — 36 (18/18). Funds the conspiracy; CONSPIRES_WITH varys built.
- `harry-strickland` — 15. GC captain-general (reluctant; cautious).
- `haldon` (Halfmaester) — 12 · `lemore` (Septa) — 12 · `rolly-duckfield` (Duck) — 7 · `ysilla` — exists. The Shy Maid crew (Aegon's tutors/guardians).
- GC officers that EXIST as nodes: `tristan-rivers`, `laswell-peake`, `marq-mandrake`, `lysono-maar`, `black-balaq`, `franklyn-flowers`, `malo-jayn`, `gorys-edoryen` (paymaster; already GUARDS landing).
- `kevan-lannister` — 35 (the assassination victim; ADWD-epilogue regent).
- Slug traps: VICTIM target is `pycelle` (NOT grand-maester-pycelle). Duck = `rolly-duckfield` (pass-1 edges may say `duck`).

## Source chapters (the lenses read these)
- **JonCon POV:** `adwd-the-lost-lord-01.md` (the reveal; the sail-west decision; Aegon's blue-dyed disguise + Illyrio's rubies), `adwd-the-griffin-reborn-01.md` (Griffin's Roost retaken; the Storm's End decision; greyscale concealment; the simultaneous-columns campaign).
- **Kevan POV:** `adwd-epilogue.md` (Varys murders Pycelle then Kevan; the "for the realm / for the children" + "Aegon raises his banner" motive).
- **Tyrion POV (the Shy Maid / Rhoyne journey):** `adwd-tyrion-03..07.md` (boards the Shy Maid; cyvasse with Young Griff; the stone-men attack tyrion-05; goads Aegon to sail west tyrion-06; grabbed by Jorah ~tyrion-07).
- **AGOT seed:** `agot-arya-03.md` (the tunnels — Varys + Illyrio conspire, Arya witnesses) — the `varys CONSPIRES_WITH illyrio` dyad is ALREADY built; only harvest quotes remain.

## The enrichment gap (what the 4 lenses go after)
1. **Secondary-character sub-arcs** (lens a): the Shy Maid crew (Haldon/Lemore/Duck/Ysilla as Aegon's guardians+tutors; TRAVELS_WITH/PROTECTS/TUTORS — careful TUTORS is for sustained 1:1); the GC officer roster + the *simultaneous-columns* command structure on the takings (Tristan Rivers→Crow's Nest, Laswell Peake→Rain House, Mandrake→Greenstone, Connington→Griffin's Roost) as COMMANDS_IN/AGENT_IN; Harry Strickland's reluctance.
2. **Whodunit/revelation** (lens b): the **Varys assassination conspiracy** (on-page) — the Rugen/undergaoler identity, the little-birds, the "for the realm" motive; the *reveal* as a revelation-event (already a node); the **greyscale concealment** as a deception/condition. NOT Aegon's identity (gated).
3. **Descriptive/quote/object depth** (lens c): Aegon's disguise (blue-dyed hair, Illyrio's 3 rubies "Red and black. Dragon colors."); JonCon's greyscale (`AFFLICTED_BY greyscale`); the Shy Maid (vessel — CAPTAIN_OF/CREW_OF?); Black Balaq's bow; the cyvasse set; Griffin's Roost; food (boiled eggs/fried bread/beans + the vinegar-wine). Object nodes likely need minting.
4. **Existing-node↔existing-node causal-wiring** (lens d, highest-value): cross-container seams. The `assassinations` 0-outgoing → the KL-endgame collapse (Kevan-regency / Cersei-Tommen); the greyscale-clock MOTIVATES JonCon's Storm's-End haste; the broken Yunkai contract → essos seam (gated re Dany convergence — TWOW, skip); the GC's Blackfyre-war founding history (Bittersteel). **Do NOT wire Aegon↔Dany convergence (TWOW/gated).**

*Baseline complete. Next: fan out the 4 Sonnet lenses (PROPOSE-don't-mint).*
