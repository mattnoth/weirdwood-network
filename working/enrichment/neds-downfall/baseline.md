# Baseline — Ned's Downfall enrichment dip (S137)

Shared dedup substrate for the 4 lenses. **Do NOT re-propose anything already here.**
The dip target is the **betrayal / conspiracy substrate** of Ned's downfall — the
actors and sub-events are *already minted nodes* but the causal links between them are
**absent**. That's the gap. The arrest→execution spine itself is built; don't re-draw it.

## The built spine (EXISTS — do not re-propose)

```
death-of-robert-baratheon  --CAUSES-->  arrest-of-eddard-stark
arrest-of-eddard-stark     --CAUSES-->  execution-of-eddard-stark
ned-confesses-to-treason   --TRIGGERS--> execution-of-eddard-stark   (+ SUB_BEAT_OF)
execution-of-eddard-stark  --CAUSES-->  robb-proclaimed-king-in-the-north
execution-of-eddard-stark  --MOTIVATES--> robb-stark
```

Role edges on `execution-of-eddard-stark` (EXIST): ilyn-payne AGENT_IN · joffrey-baratheon
COMMANDS_IN · eddard-stark VICTIM_IN · ice WIELDED_IN · sansa-stark WITNESS_IN · LOCATED_AT
great-sept-of-baelor.

Role edges on `ned-confesses-to-treason` (EXIST): eddard-stark AGENT_IN · cersei-lannister
COMMANDS_IN ("a tame wolf is of more use than a dead one") · LOCATED_AT great-sept-of-baelor.

## The arrest cluster (`arrest-of-eddard-stark`) — 4 SUB_BEAT_OF children (EXIST)

All four are wired `SUB_BEAT_OF arrest-of-eddard-stark`. Their internal role edges exist; the
**causal links between them and outward are the gap.**

1. `cersei-orders-ned-s-arrest` (event.capture) — cersei COMMANDS_IN · barristan-selmy AGENT_IN
   · eddard VICTIM_IN.
2. `gold-cloaks-betray-ned` (event.conspiracy) — gold-cloaks / janos-slynt / sandor-clegane
   AGENT_IN · cersei-lannister + petyr-baelish COMMANDS_IN · eddard / tomard / varly VICTIM_IN.
3. `ned-orders-janos-slynt-to-arrest-cersei` (event.capture) — eddard COMMANDS_IN · janos-slynt
   AGENT_IN · cersei VICTIM_IN. (Ned's order that Slynt betrays.)
4. `littlefinger-betrays-ned` (event.incident) — petyr-baelish AGENT_IN. **ONLY 2 edges total,
   NO forward CAUSES.** ("Littlefinger slid Ned's dagger from its sheath and shoved it up under
   his chin", agot-eddard-14:125.)

Also incoming to the arrest: `death-of-robert-baratheon CAUSES` (above). Outgoing: PART_OF
war-of-the-five-kings · PRECEDES battle-on-the-green-fork.

## CAUSAL ISLANDS — the high-value gap (0 or near-0 causal edges)

- **`ned-discovers-the-truth-of-joffrey-s-parentage`** (event.incident) — THE central revelation.
  Edges: eddard AGENT_IN · MOTIVATES eddard-stark ("I intend to lay the truth before him") ·
  MOTIVATES cersei-lannister ("you win or you die"). **NO causal link forward to the arrest or
  to Cersei's move.** This is the engine of the whole arc and it is causally islanded.
- **`varys-confirms-cersei-s-role-in-robert-s-death`** — 0 outgoing edges. (Black-cells scene:
  Varys visits the condemned Ned.)
- **`cersei-orders-the-sleeping-guards-executed`** — 0 outgoing edges.
- `ned-claims-the-execution` — this is the DESERTER beheading at the START of AGOT (Gared, agot-bran-01
  / Darry), **NOT** Ned's own execution. Do not conflate.

## Other existing nodes in/near the cluster (dedup — already minted)

`pycelle-arrested-and-thrown-in-the-black-cells` · `jaime-frees-tyrion-from-the-black-cells`
(later arc) · `attack-on-ned-stark-in-the-streets-of-kings-landing` (the Jaime street-brawl,
EARLIER — Ned's leg wound) · `ned-opposes-the-assassination` / `ned-orders-daenerys-s-assassination-cancelled`
(the small-council Daenerys arc, EARLIER) · `execution-of-janos-slynt` (ADWD, Jon's arc — NOT here).

## Downstream anchors already wired (for lens-4 forward-wiring)

`robb-proclaimed-king-in-the-north` (execution CAUSES) · `robb-stark` (execution MOTIVATES).
The execution already feeds the WO5K. **Lens-4 opportunity = wire the BETRAYAL substrate forward
into Joffrey's reign / the WO5K, NOT re-draw arrest→execution.**

## Nodes that may NOT have a home yet (possible mints — propose with dedup note)

- **Renly's throne-room offer** — Renly offers Ned 100 swords to seize Joffrey and Cersei the
  night Robert dies; Ned refuses (agot-eddard-13). No event node found. (Candidate mint OR
  role-attach — propose, flag dedup.)
- The **gold-cloak / Janos Slynt bribery** mechanic (Littlefinger bought the City Watch) — is it
  captured by `gold-cloaks-betray-ned` (petyr COMMANDS_IN) or does it want its own beat? Lean
  toward role/causal wiring on the existing node, not a new node.

---

## RELEVANT SOURCE CHAPTERS (read these for verbatim quotes)

- `sources/chapters/agot/agot-eddard-12.md` — Ned proves Joffrey's parentage (the books / "All
  three are Jaime's") + the godswood confrontation with Cersei ("you win or you die").
- `sources/chapters/agot/agot-eddard-13.md` — Robert's dying; Renly's offer of 100 swords; Ned
  refuses; Littlefinger's counsel; the regency-letter ("Protector of the Realm").
- `sources/chapters/agot/agot-eddard-14.md` — the throne-room betrayal: Slynt's gold cloaks turn,
  Littlefinger's dagger to Ned's throat, the household-guard massacre (Tomard, Varly, Cayn), arrest.
- `sources/chapters/agot/agot-eddard-15.md` — Ned in the black cells; Varys's visit (Cersei got
  Robert drunk via Lancel; the strongwine); Varys pushes Ned toward the false confession to save Sansa.
- `sources/chapters/agot/agot-arya-05.md` — the false confession + execution at the Sept of Baelor.
- `sources/chapters/agot/agot-sansa-04.md` — Sansa's plea to Joffrey; Joffrey's promise of "mercy".
- `sources/chapters/agot/agot-sansa-06.md` — aftermath; Sansa watches the gold cloaks fling Ned down.
</content>
