# Baseline — A2.2 Sansa / Vale build+enrich (S148)

> The descent's first **build+enrich** dip (no spine exists yet). Build the causal skeleton FIRST,
> then enrich. Highest cross-arc payoff per dip: fixes the longest-orphaned node
> (`littlefinger-smuggles-sansa-out-of-kings-landing`), the hairnet chain, and builds most of the
> Petyr Baelish web (C2). Source chapters: ASOS Sansa V–VII + AFFC Sansa I / Alayne I–II.

## The dead-end (what the dip fixes)

- **`littlefinger-smuggles-sansa-out-of-kings-landing`** (event.deception) — 2 out / 4 in.
  OUT = `LOCATED_AT red-keep`, `SUB_BEAT_OF purple-wedding`. **No downstream into the Vale at all.**
  IN = petyr/dontos AGENT_IN, `death-of-joffrey TRIGGERS`, sansa VICTIM_IN. → The longest-orphaned node.
- **`wedding-of-petyr-baelish-and-lysa-arryn`** (event.wedding) — 0 out / 1 in (only a junk `PRECEDES`
  from battle-on-the-green-fork). No participants, no causal wiring.
- **`lord-nestor-and-the-knights-call-for-marillion-s-death`** (event.death) — 0 out / 3 in
  (nestor AGENT_IN, petyr COMMANDS_IN, marillion VICTIM_IN). **No upstream cause** — it's the FRAMING
  for Lysa's death, but `death-of-lysa-arryn` **has no node**.
- **`sansa-receives-the-poisoned-hairnet`** (event.deception) — already wired into the Purple Wedding
  (CAUSES death-of-joffrey). The hairnet chain currently terminates at the smuggling dead-end.

## Spine gaps — nodes likely to MINT (lenses confirm/refine)

1. `death-of-lysa-arryn` (event.death / event.assassination?) — Littlefinger pushes Lysa through the
   Moon Door (asos-sansa-07). THE missing keystone. POV-confirmed act ("Only Cat"), Marillion framed.
2. `sansa-assumes-the-alayne-stone-identity` (event.deception or identity node) — the Alayne persona
   (PW pass-2 ledger candidate). Pairs with the `alayne-baelish` SAME_AS/cross-identity case.
3. (maybe) the arrival/sheltering at the Fingers; LF's trial before the Lords Declarant; the descent
   from the Eyrie; the Harry-the-Heir betrothal plan (affc-alayne-02). Lenses decide which warrant nodes.

## Existing nodes (use as-is — dedup map)

**Events:** `littlefinger-smuggles-sansa-out-of-kings-landing` · `wedding-of-petyr-baelish-and-lysa-arryn`
· `lord-nestor-and-the-knights-call-for-marillion-s-death` · `sansa-receives-the-poisoned-hairnet`
· `lysa-accuses-tyrion-of-poisoning-jon-arryn` · `murder-of-jon-arryn` (S133, the founding crime) ·
`littlefinger-betrays-ned` · `littlefinger-brokers-tyrell-lannister-alliance` ·
`littlefinger-names-the-dagger-as-tyrion-s` · `joffrey-sets-sansa-aside-and-agrees-to-wed-margaery`.
**`alayne-i-the-winds-of-winter`** = a TWOW event node — **TWOW is unpublished; do NOT wire as canon spine.**

**Characters:** `sansa-stark` (179 edges, socially saturated / 0 Vale-arc-connected) · `petyr-baelish`
(109 — the C2 build target) · `lysa-arryn` (54) · `robert-arryn` (Sweetrobin, 24) · `marillion` (15) ·
`harrold-hardyng` (14, aliases Harry the Heir/Young Falcon) · `dontos-hollard` · `nestor-royce`.

**DEDUP TRAPS (critical):**
- `alayne-baelish` = Sansa's Alayne persona → **SAME_AS/cross-identity case** (high-stakes; propose the
  edge, do NOT silently merge). `alayne` (wiki disambiguation) and `alayne-royce` (a real Royce) are
  **DIFFERENT** — do NOT conflate either with Sansa.
- `robert-arryn` (Sweetrobin) is the node. `robin-arryn` is a **separate historical Arryn** — do NOT use.
- No standalone `littlefinger` node — it's an alias on `petyr-baelish`. Use `petyr-baelish`.

**Locations/factions/objects:** `eyrie` · `vale-of-arryn` · `godswood-of-the-eyrie` · `moon-door`
(artifact) · `brotherhood-of-winged-knights` (faction) · `the-fingers`? (check) ·
`lord-protector-of-the-eyrie-and-the-vale-of-arryn` (title).

## Container tag: NONE

Vale is **not** one of the 5 approved containers (essos/wo5k/north/aegon/bran). Do NOT add a
`containers:` tag and do NOT invent a "vale" container (per the DO-NOT list).

## Chapter map

| File | ASOS/AFFC ch | Arc content |
|------|:---:|---|
| asos-sansa-05 | ASOS 62 | Purple Wedding death of Joffrey; Sansa flees with Dontos |
| asos-sansa-06 | ASOS 69 | aboard ship → the Fingers; LF reveals the plot; kills Dontos; the hairnet reveal |
| asos-sansa-07 | ASOS 81 | the Eyrie; LF weds Lysa; the snow castle / the kiss; **Lysa's death via the Moon Door**; Marillion framed |
| affc-sansa-01 | AFFC 11 | aftermath; Lord Nestor; Marillion's coerced confession; LF's trial before the Lords Declarant |
| affc-alayne-01 | AFFC 24 | the Eyrie in winter; Sweetrobin's shaking sickness; the descent prep; Lyn Corbray; the Lords Declarant pact |
| affc-alayne-02 | AFFC 42 | Gates of the Moon; **the Harry-the-Heir betrothal plan**; Myranda Royce; the tourney of the Winged Knights |

## Vocab + conventions (locked)

- Locked vocab: `working/wiki/data/edge-type-counts.md` (170 canonical types). Verify membership against
  the schema — edges.jsonl uses `edge_type`/`source_slug`/`target_slug`, NOT `type`.
- `MOTIVATES` target = the **person/actor**, not the event (route grievance through the human).
- `SUSPECTED_OF` (Tier-2) = unproven-but-load-bearing agency — never asserts the act.
- `GIFTED_TO` live direction = **giver → recipient** (not architecture's artifact→recipient). Check live
  direction before emitting any artifact-transfer edge.
- `DISGUISED_AS` / `IMPERSONATES` for the Alayne persona; `SAME_AS` symmetric for the identity case.
- Theory readings stay GATED (no fAegon/R+L/Azor-Ahai; no "Sansa-is-secretly-X"). Evidence edges only.
