# Baseline — D1 Battle of Castle Black enrichment dip (S153)

> The ASOS Wall defense — Mance's two-pronged assault on Castle Black (Styr's Thenns from the
> south + Mance's main host at the gate from the north), Ygritte's death, Donal Noye killing
> Mag the Mighty in the tunnel, Grenn holding the gate, Stannis's relief charge.
> **Class D top pick (Matt-picked S153).** Baselined this session (Class-D clusters are NOT
> graph-verified). edges.jsonl = 22,988 at dip start. Vocab = 170 canonical types.

## TL;DR — the shape of the gap
The cluster's **social/dyad layer is DENSE** (Jon Snow's web — 348 edges — lives largely here:
RESPECTS/TRUSTS/MOURNS/LOVES/HATES across Noye, Ygritte, Mance, Styr, Qhorin, Grenn, Pyp, Aemon).
But the **EVENT-HUB structure is THIN and the marquee beats are under-reified or missing**:
the battle hub has no causal *upstream*, several iconic beats exist only as character-dyads
(Noye↔Mag mutual kill) with **no event node**, Ygritte's death has **no node** (only `MOURNS` +
wiki `DIED_AT`), and the southern Thenn assault (where Ygritte + Styr die) has **no node at all**.
This is a build+enrich on the event layer over an already-dense social layer.

## Core node-set (what exists)

### The hub + its 5 sub-beats (northern gate assault)
- `attack-on-castle-black` (event.battle, tier-1, `containers: [north, jon]`) — **HUB**. Rich prose
  Origins + Aftermath (documents the whole battle incl. the southern Thenn climb/assault, Ygritte's
  death, the scarecrow-sentinels ruse, Aemon's letters). Edge layer thin:
  - OUT: `CAUSES battle-beneath-the-wall` [tier-3, weak quote] · **JUNK** `PRECEDES battle-near-yunkai`
  - IN: 5× `SUB_BEAT_OF` · **JUNK** `battle-at-the-burning-septry PRECEDES →`
  - Stray off-vocab `## Edges` block in the node file (`FIGHTS_IN: Conflict beyond the Wall`,
    `DEFEATS: Castle Black` — Pass-2 infobox parse artifacts, never became real edges; node-prose noise).
- `night-battle-atop-the-wall` (event.battle) — Jon commands archers atop the Wall; Noye COMMANDS_IN; nights-watch/free-folk AGENT_IN
- `mammoth-attacks-gate-below` (event.incident) — Grenn+Pyp roll burning oil; Noye COMMANDS_IN
- `wildlings-attack-the-gate` (event.incident) — Pyp spots them; Grenn+Pyp+free-folk AGENT_IN; Noye COMMANDS_IN
- `deaf-dick-follard-killed` (event.death) — dick-follard VICTIM_IN (arrow on the crenel)
- `lightning-strikes-the-tower-direwolf-attacks` (event.incident, asos-jon-05 Queenscrown) — Ghost AGENT_IN kills a Thenn; del + unnamed-thenn VICTIM_IN

### The relief + downstream (well-wired into NORTH spine)
- `battle-beneath-the-wall` (event.battle) — Stannis's cavalry charge. IN: `attack-on-castle-black CAUSES` + `stannis-moves-to-the-wall CAUSES`. OUT: `CAUSES mance-rayder-brought-to-execution`, `ENABLES jon-elected-lord-commander`, `ENABLES fight-by-deepwood-motte`, `PART_OF war-of-the-five-kings`.
- `stannis-moves-to-the-wall` (event.incident) — `CAUSES battle-beneath-the-wall`; `stannis-retreats-to-dragonstone ENABLES →`
- `mance-rayder-brought-to-execution` (event.execution, ADWD) — the glamour-swap terminus; `ENABLES pink-letter-delivered`

### Queenscrown beat — OVER-FRAGMENTED (3 nodes, 1 scene, asos-jon-05)
- `ygritte-kills-the-old-man` (event.death) — ygritte AGENT_IN, styr COMMANDS_IN, old-man VICTIM_IN
- `styr-orders-jon-to-kill-the-old-man` (event.death) — jon AGENT_IN("No"), styr COMMANDS_IN, old-man VICTIM_IN
- `jon-refuses-to-kill` (event?) — jon AGENT_IN, styr+ygritte COMMANDS_IN
  → **Three nodes for one beat.** Styr orders → Jon refuses → Ygritte does it. Consolidation candidate (synthesis decides; retiring nodes = structural surgery, fresh-verify gate).

### Skirling-Pass islands (ACOK, Qhorin arc — adjacent, 0-outgoing)
- `jon-spares-ygritte` (event.execution, acok-jon-06) — Jon captures Ygritte, refuses Qhorin's order to kill her. qhorin COMMANDS_IN, jon+ebben AGENT_IN, ygritte VICTIM_IN.
- `attack-on-the-wildlings` (event.incident, acok-jon-06) — Qhorin's group raids the watchers; jon+stonesnake AGENT_IN, longclaw WIELDED_IN.
  → These belong to the **great-ranging / Qhorin's-Halfhand arc** (how Jon got among the wildlings), NOT the Battle of Castle Black proper. Candidate wiring is to `great-ranging`, not the battle. **Scope-watch — don't pull the whole Qhorin arc into this dip.**

### Upstream (causal lead-in candidate)
- `great-ranging CAUSES fight-at-the-fist` [tier-2] exists. `fight-at-the-fist` is the Watch-strength-wiped-out event the hub's Origins names as the *reason* Mance attacks. The hub has **NO causal upstream** — `fight-at-the-fist ENABLES attack-on-castle-black` (weakened garrison) is the clean lens-4 seam. (Note possible dup `fight-at-the-fist` vs `battle-of-the-fist-of-the-first-men` — out of scope, flag only.)

## Key dyads that ALREADY exist (do NOT re-mint — dedup!)
- `donal-noye KILLS mag-mar-tun-doh-weg` AND `mag-mar-tun-doh-weg KILLS donal-noye` — **the mutual tunnel-death dyad is BOTH directions wired** (asos-jon-08:171). Missing = the *event hub* reifying it.
- `jon-snow MOURNS ygritte` (asos-jon-08:13); `jon-snow MOURNS donal-noye`; `stannis-baratheon MOURNS donal-noye`.
- `jon-snow HATES styr`; `jon-snow SERVES styr` (the pretence); `styr DIED_AT castle-black`; `ygritte DIED_AT castle-black` (both wiki).
- Jon's dense relationship web (RESPECTS/TRUSTS/LOVES/LOVER_OF/PROTECTS) with Ygritte, Noye, Mance, Qhorin, Grenn, Pyp, Aemon, Stonesnake, Satin — **saturated, leave it.**

## THE GAP — what a dip adds (proposal targets)

**A. Reify the marquee beats that exist only as dyads / not at all:**
1. **Death of Ygritte** (asos-jon-07) — dies of an arrow in Jon's arms ("You know nothing, Jon Snow"); Jon burns her body north of the Wall. Only `MOURNS` + wiki `DIED_AT` exist → mint the event.death node; who shot her (unknown/own side — leave un-attributed or SUSPECTED_OF), jon WITNESS_IN, jon burns-the-body beat.
2. **Death of Donal Noye / the tunnel fight** (asos-jon-08) — Noye & Mag the Mighty kill each other in the gate tunnel. Dyad exists both ways → **reify the event hub** (noye + mag AGENT_IN + VICTIM_IN; SUB_BEAT_OF the battle hub); the iconic "they died together" beat.
3. **The southern Thenn assault on Castle Black + Jon kills Styr** (asos-jon-07) — currently NO node; this is where Ygritte dies. `jon KILLS styr` is **absent** (verified — only HATES/SERVES). Mint the southern-assault beat; jon AGENT_IN; styr VICTIM_IN; styr's death.
4. **Grenn holds the inner gate** (asos-jon-09, "the boys" hold the tunnel against the giant) — iconic; partially in `mammoth-attacks-gate-below` but the tunnel-hold is distinct.
5. **Jon takes command of the defense** after Noye's death (asos-jon-09) → already `battle-beneath-the-wall ENABLES jon-elected-LC`, but the in-battle command transfer is its own beat.
6. **Jon's parley/assassination sortie to Mance** (asos-jon-09) — Jon goes out under the guise of treating with Mance, planning to kill him; the night Stannis arrives.

**B. Causal wiring (lens 4):**
- `fight-at-the-fist ENABLES attack-on-castle-black` (the Watch wiped out → Mance attacks) — fixes the no-upstream gap.
- Bowen Marsh marching the garrison out (the Origins ruse) weakened the castle → enabling beat (no node; candidate).
- Southern-assault → northern-gate-assault relationship (two-pronged simultaneity — CONTEMPORARY_WITH or shared-hub).
- Possible upgrade of `attack-on-castle-black CAUSES battle-beneath-the-wall` (tier-3, weak quote → tier-2 with a better cite).

**C. Hygiene (finalize step):**
- **RETIRE** 2 junk PRECEDES: `attack-on-castle-black PRECEDES battle-near-yunkai` + `battle-at-the-burning-septry PRECEDES attack-on-castle-black` (cross-theater chronology artifacts).
- **Consolidate** the Queenscrown triple-dup (3 nodes → 1, aliases/SUB_BEAT for nuance).
- Flag (NOT this dip): `fight-at-the-fist` vs `battle-of-the-fist-of-the-first-men` possible dup.

**D. Quote/object depth (lens c + harvest):**
- Ygritte's "You know nothing, Jon Snow" death line (iconic).
- Donal Noye's last stand; the scarecrow sentinels (Aemon's ruse); the oil-barrels; Mag the Mighty + the giants + mammoths descriptions; Satin helping Jon from the King's Tower.
- Food/grim register: Mole's Town refugees, siege rations.

## Chapter pointers (read these directly)
- `sources/chapters/asos/asos-jon-05.md` — Queenscrown: Jon refuses to kill the old man, Ygritte kills him, lightning/Ghost, Jon escapes
- `asos-jon-06.md` — Jon rides wounded to Castle Black; warns of the southern attack; Aemon heals him
- `asos-jon-07.md` — **the southern Thenn assault**; Jon kills Styr (verify); **Ygritte's death**
- `asos-jon-08.md` — **the northern gate assault**; mammoth, oil, night battle atop the Wall; **Noye kills Mag in the tunnel** (both die)
- `asos-jon-09.md` — Jon takes command; Grenn holds the gate; Jon's sortie to Mance
- `asos-jon-10.md` — Jon in Mance's camp; **Stannis's relief charge** (battle beneath the Wall)
- `asos-jon-11.md` — aftermath; Stannis offers terms; Mance/execution
- Wiki: `sources/wiki/_raw/Attack_on_Castle_Black.json`, `Battle_beneath_the_Wall.json`

## Internal cluster edges (deduped) — 180 edges within the core set
(Full dump: `working/enrichment/battle-castle-black/internal-edges.txt`. The dense social web is
intact; the thin layer is event-hubs + causal wiring, per the gap above.)
