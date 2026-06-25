# Jon Snow / the Wall enrichment — DEDUP BASELINE (S145)

> **PROPOSE, don't mint.** Everything below ALREADY EXISTS in the graph. Do NOT re-propose it.
> Verify any node you want to propose: `find graph/nodes -name "<slug>.node.md"` (exists → don't mint)
> and check `graph/edges/edges.jsonl` for the edge before proposing it. When in doubt, dedup-check.

## The built NORTH spine (event nodes — DO NOT re-mint)
From `--container north` (19 nodes):
- `great-ranging` → `fight-at-the-fist` → `mutiny-at-crasters-keep` (Craster's mutiny, ASOS)
- `attack-on-castle-black` · `battle-beneath-the-wall` (Stannis routs the wildlings)
- `jon-elected-lord-commander` → `execution-of-janos-slynt`
- `jon-allows-free-folk-through-the-wall` (the decree)
- `pink-letter-delivered`
- `jon-is-stabbed-repeatedly` (the Bowen-Marsh assassination, ADWD — **canonical**; `mutiny-at-castle-black` is the SEPARATE Craster's-Keep ASOS node — DO NOT conflate)
- `mance-rayder-brought-to-execution`
- `roose-named-warden-of-the-north` · `stannis-moves-to-the-wall` · `stannis-march-on-winterfell` · `stannis-s-army-stalls-at-crofters-village`
- (+ wo5k/bran-tagged: `capture-of-winterfell`, `sack-of-winterfell`, `robb-proclaimed-king-in-the-north`, `balon-declares-himself-king`, `ironborn-invasion-of-the-north`)

## Existing causal/role substrate around the stabbing (DO NOT re-propose)
- `jon-allows-free-folk-through-the-wall MOTIVATES bowen-marsh`  (the grievance — adwd-jon-13:149)
- `execution-of-janos-slynt MOTIVATES bowen-marsh`  (per S126)
- `pink-letter-delivered TRIGGERS jon-is-stabbed-repeatedly`  (the Shieldhall march call — adwd-jon-13:295)
- `bowen-marsh AGENT_IN jon-is-stabbed-repeatedly`
- `wick-whittlestick AGENT_IN jon-is-stabbed-repeatedly`
- `jon-snow VICTIM_IN jon-is-stabbed-repeatedly`
- `jon-is-stabbed-repeatedly LOCATED_AT castle-black`

## The GAP this dip fills (what's THIN / MISSING — propose here)
- **`the-shieldhall-speech` — MISSING.** Mint as the explicit trigger beat (currently Pink Letter TRIGGERS the stabbing directly, collapsing the Shieldhall speech). Wire Jon's march-on-Winterfell call → the stabbing; conspirators react.
- **More conspirators / the SUSPECTED_OF layer.** Only Bowen Marsh + Wick Whittlestick are AGENT_IN. Othell Yarwyck (EXISTS), the Bowen faction, the "for the Watch" knot — propose AGENT_IN / SUSPECTED_OF as the text supports (Tier-2 for unproven agency; never assert beyond the text).
- **The Mance / "Rattleshirt" glamour.** `rattleshirt` node MISSING; `mance-rayder` EXISTS, `melisandre` EXISTS, `varamyr` EXISTS. Melisandre glamours Mance as Rattleshirt (the Lord of Bones); the burned man is Rattleshirt. Consider IMPERSONATES / disguise edges + Melisandre AGENT_IN the glamour. (adwd-melisandre-01, adwd-prologue/Varamyr.)
- **Hardhome** (`hardhome` location EXISTS; no event node) — the wildling-rescue catastrophe / the Hardhome letter as a revelation-beat.
- **Stannis-at-the-Wall texture** — Stannis's offer of Winterfell / legitimization; Jon's refusal. `stannis-baratheon`, `selyse-florent`, `melisandre` EXIST.
- **Wildling-integration politics** — the cost of the free-folk decision to Jon's standing. `tormund` (slug = `tormund`, NOT `tormund-giantsbane`), `val`, `wun-weg-wun-dar-wun` (the giant) all EXIST.
- **Slynt-execution color** (`execution-of-janos-slynt` EXISTS — add participant/witness texture only).

## Slug traps (use these EXACT slugs)
- `selyse-florent` (NOT selyse-baratheon) · `tormund` (NOT tormund-giantsbane) · `wun-weg-wun-dar-wun` (the giant Wun Wun)
- `shieldhall` = the LOCATION node (exists); `the-shieldhall-speech` = the EVENT node to mint (does not exist)
- `jon-is-stabbed-repeatedly` is the ADWD assassination; `mutiny-at-castle-black` is the ASOS Craster's mutiny — never merge

## Theory gate
Jon's parentage (R+L=J) and Azor Ahai / Lightbringer stay **GATED** — evidence edges only, NO theory readings/assertions.
