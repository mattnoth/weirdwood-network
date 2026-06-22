# Continue — NORTH spine build, part 2 (N3 + N4: Jon's Lord-Commander era → the stabbing)

> **Recommended model:** Sonnet 4.6 subagents for research/verify; orchestrator coordinates. (Same arc-mint
> machine as N5/N2/N1, S125, and WO5K-remainder, S123.)
> **This is a BUILD session — it mutates the graph** (mints nodes + edges + executes one node merge).
> **Prereq:** probe one trivial subagent first (API-health), then go.

## State (after S125)
The NORTH **top-3 junctures are BUILT** (N5 Roose-Warden / N2 Stannis-at-the-Wall / N1 great-ranging-wire) —
see worklog S125. Container `north` = 13 nodes. The WO5K→NORTH seam now traverses end-to-end:
`stannis-retreats-to-dragonstone ENABLES stannis-moves-to-the-wall CAUSES battle-beneath-the-wall CAUSES
mance-rayder-brought-to-execution`. **Spec for everything below: `working/north-decomposition.md`** (N3 = §3 Rank 4,
N4 = §3 Rank 5; nodes-to-mint table §7). Read it first.

This session builds the **Jon Lord-Commander spine** — from the LC election through the ADWD authority beats to
the NORTH terminus (the stabbing). N3 extends naturally from the N2 battle; N4 is the climactic terminus arc.

## Task — build N3 then N4 (in order), fresh-verify every causal edge

### N3 (Rank 4, score 10/12) — LC Election → Slynt Execution → Jon's authority established
- **1 mint:** `jon-elected-lord-commander` (event.ceremony; ASOS Jon XII — "the 998th Lord Commander of the
  Night's Watch"; Sam engineers the vote against Slynt). Container `[north, jon]`.
- **Edges (research + fresh-verify):**
  - `battle-beneath-the-wall ENABLES jon-elected-lord-commander` — the battle's aftermath (Mormont dead since
    Craster's, Stannis present pressuring the vote) is the precondition for the election. (Node Aftermath already
    states "the Night's Watch... start the vote for Jeor's successor.") Weigh ENABLES vs CAUSES.
  - `jon-elected-lord-commander CAUSES execution-of-janos-slynt` — LC authority is the prerequisite for Jon to
    execute Slynt for refusing orders. (Granularity: prior prerequisite, not constitutive → CAUSES is right.)
  - `jon-elected-lord-commander MOTIVATES jon-snow` (agency: Jon chooses to enforce his authority) + role
    `jon-snow AGENT_IN jon-elected-lord-commander`.
- **Attach:** `battle-beneath-the-wall` (HIT) / `execution-of-janos-slynt` (HIT — already has the "Longclaw
  descended." + Stannis-nod quotes attached in the S125 harvest pass).
- Dedup-check first: confirm no wiki node already exists for the election (grep `graph/nodes/events/` for
  "lord commander" / "election" / "choosing"; `jon-overhears-the-conspiracy` EXISTS and is the catalyzing beat
  — connect upstream if the text supports it, but it is NOT the election itself).

### N4 (Rank 5, score 10/12, larger scope) — Free Folk through the Wall → Pink Letter → the Stabbing (NORTH terminus)
- **RESOLVE THE DEDUP FIRST (carried from S124/S125, decision recorded):** `mutiny-at-castle-black` and
  `jon-is-stabbed-repeatedly` are the **same ADWD event**. **Canonical = `jon-is-stabbed-repeatedly`** (it carries
  the curated role-edge structure — `jon-snow VICTIM_IN`, `bowen-marsh`/`wick-whittlestick AGENT_IN`, BETRAYS edges,
  LOCATED_AT castle-black — and is the SHAPE-map NORTH terminus; it now also has the "For the Watch." stabbing quote
  from the S125 harvest). `mutiny-at-castle-black` is a tier-1 wiki node with rich Origins prose but only **1 junk
  PRECEDES edge** (`battle-on-the-green-fork PRECEDES mutiny-at-castle-black` — a bogus chronology artifact). **MERGE:**
  port the tier-1 wiki Origins prose from `mutiny-at-castle-black` into `jon-is-stabbed-repeatedly` (which is a bare
  Plate-3 stub body); add "Mutiny at Castle Black" + the wiki_source as aliases/same_as on the survivor; drop or
  repoint the junk PRECEDES edge; rebuild indexes + alias resolver after the rename/merge. **`mutiny-at-crasters-keep`
  is the DISTINCT ASOS Mormont mutiny — DO NOT touch it.**
- **2 mints:**
  - `jon-allows-free-folk-through-the-wall` (event.decree; ADWD Jon XII — "Four thousand wildlings would come
    pouring through the Wall. Madness." — harvest row parked at adwd-jon-12:23). `[north, jon]`. NOTE the existing
    partial node `hostage-boys-pass-through` (the hostage-exchange moment) — decide enrich-vs-mint: the primary
    decision (opening the gate) may warrant the new node distinct from the hostage beat. Flag for the research dip.
  - `pink-letter-delivered` (event.incident; ADWD Jon XIII — harvest rows parked at adwd-jon-13:227 arrival +
    adwd-jon-13:295 Shieldhall announcement). `[north]` (NOT a bridge per the SHAPE map). Dedup vs the
    `bastard-letter` ARTIFACT node (which exists — the letter object; the new node is the receiving/reading EVENT).
- **Edges (agency-collapse care — these MOTIVATES are load-bearing; do NOT collapse to a blunt CAUSES):**
  - `execution-of-janos-slynt MOTIVATES bowen-marsh` (seeds the mutiny's grievance) — verify.
  - `jon-allows-free-folk-through-the-wall MOTIVATES bowen-marsh` (the direct provocation that tips the conservatives).
  - `pink-letter-delivered TRIGGERS jon-is-stabbed-repeatedly` (Jon's march announcement → the mutineers act "For
    the Watch"). The Pink Letter is the specific spark → TRIGGERS.
  - Consider `jon-allows-free-folk-through-the-wall CAUSES`/contributes to the mutiny via the Bowen-Marsh agency
    chain — let fresh-verify adjudicate the exact topology (the dip flags high agency-collapse risk here).
- **Terminus:** `jon-is-stabbed-repeatedly` (the NORTH hard terminus). Do NOT wire into TWOW (no resurrection).

## Hard rules (same as S125)
- Edge types ONLY: **CAUSES / TRIGGERS / ENABLES / MOTIVATES** (MOTIVATES target = a character) + roles
  AGENT_IN / VICTIM_IN / COMMANDS_IN / WITNESS_IN. Never invent types.
- **FIRM fresh-verify** on every causal edge (separate read-only subagent CONFIRM/ADJUST/REJECT vs LOCAL cache;
  Matt gates at policy, not per-edge). **Dedup before every mint** (`event_alias_resolver.py --lookup` + grep
  `graph/nodes/events/`). Granularity policy (S120): constitutive beat → SUB_BEAT_OF only; prior prerequisite →
  CAUSES/TRIGGERS. Agency-collapse check per juncture.
- **Quote rule for research subagents:** a SINGLE CONTIGUOUS substring, never spliced across a dialogue
  attribution (`," said X, "`) — it breaks `verify-edge-quotes`. Line-check every cite.
- Stamp `containers:` at mint (`[north, jon]` for Jon-authority beats, `[north]` for the Pink Letter).
  Node aliases = natural SPACED phrases, not kebab.
- **Machine:** research dip → `scripts/mint_*_arc.py` (use `mint_arc_lib.precheck_slugs`; backup + re-run guard;
  `verified_by: pending-*` until fresh-verify, then stamp `fresh-subagent-confirm-2026-06-24-n{3,4}`) →
  `verify-edge-quotes.py --run-id` → rebuild indexes (`build-entity-indexes.py --type events --all`) + alias
  resolver (`event_alias_resolver.py --build`) → `stamp_containers.py` → `--causal-chain`/`--full-chain` smoke.
  Template: `scripts/mint_north_spine_s125.py`.

## Harvest — parked rows this build will UNBLOCK (flip to open + attach as you mint)
In `working/harvest-queue.md` (SET B from S125, parked awaiting these nodes):
- adwd-jon-13:227 (Pink Letter arrival) → `pink-letter-delivered` ## Quotes
- adwd-jon-13:295 (Jon's Shieldhall march announcement) → `pink-letter-delivered` or a march node ## Quotes
- adwd-jon-12:23 (Jon's free-folk monologue, "Madness.") → `jon-allows-free-folk-through-the-wall` ## Description/Quotes
- (agot-jon-07:147 Watch oath stays parked — its home `jon-joins-the-nights-watch` is not in N3/N4 scope)
- (asos-jon-11:109 Stannis "cart before the horse" foreshadowing — stays parked, no node target)

## DO NOT
Refetch the wiki (cache is local at `sources/wiki/_raw/`) · build a White-Walkers/Others arc · model Jon's
resurrection or any TWOW material (`jon-is-stabbed-repeatedly` is the hard terminus) · pull R+L=J / the
greenseer thread into NORTH · mass-mint (N3 then N4 only, re-dip after) · `/endsession` without explicit permission.

## At session end
Update worklog (S126 entry + STATUS counts; archive the oldest session entry — S121 will be the 6th-out, → archive025
[has room: S117–S120]) · archive this prompt · hand off the NEXT NORTH junctures (N6 Stannis-marches-south, or the
Theon/Jeyne escape) OR pivot to AEGON (fix the `PART_OF war-of-five-kings` edge bug first) / Bran decomp — Matt picks.

## Reference
Spec: `working/north-decomposition.md` (N3 §3 Rank 4, N4 §3 Rank 5, §7 mint table). Template build: worklog S125 +
`scripts/mint_north_spine_s125.py`. Arc-mint machine: `progress/continue-prompts/archive/2026-06-18-causal-arc-execution.md`
+ `scripts/mint_arc_lib.py` + `scripts/stamp_containers.py`. Scorecard rubric: `working/causal-arc-strategy-2026-06-18.md`.
