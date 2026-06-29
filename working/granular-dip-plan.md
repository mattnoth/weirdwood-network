# Granular-Dip Plan — the ranked, graph-grounded descent list (S168)

> **The granular-phase analogue of `working/enrichment-coverage-plan.md`** (which was the arc-phase
> planning deliverable). The 🅰 **A-roundup is CLOSED** (S167 — 27 major-arc dips; graph at 23,330 edges /
> 8,475-ish live nodes). Per Matt's S130 plan, a dedicated PLANNING session sits between the arc phase and
> the granular phase: scope the descent to the granular tier now that the arc enrichments have built most
> major character webs as a by-product.
>
> **PLANNING ONLY — nothing minted as enrichment this session.** (STEP 0 harvest drain ran separately:
> 39→0; +2 FORESHADOWS edges, all else node-prose; see worklog S168.) The census below is read-only
> graph-grounding (`graph-query.py` / direct `edges.jsonl` scan).
>
> **Vocab:** a *dip* = one focused enrichment pass over one unit; *spine* = the bare causal skeleton
> (event nodes wired CAUSES/TRIGGERS/MOTIVATES/ENABLES) without side-plot/participant/whodunit depth.
> Class B = L2 sub-plot inside an enriched arc; Class C = cross-cutting character web; Class D = big event
> cluster no single POV owns. Confidence ratings are 1–5 only (not used here for work-priority).

---

## Graph-grounding census (verified S168, direct `edges.jsonl` scan)

`deg` = total edges touching the node; `causal` = edges of type CAUSES/TRIGGERS/MOTIVATES/ENABLES/
FORESHADOWS/PRECEDES/SUB_BEAT_OF touching it.

| candidate | slug | deg | causal | read |
|-----------|------|:---:|:---:|------|
| **D2 Hand's Tourney** | `the-hands-tourney` | 33 | **0** | dense ROSTER (26 FIGHTS_IN + 6 ATTENDS + 1 LOCATED_AT), **zero event-beats, zero causal** |
| **D3 Greyjoy's Rebellion (rich)** | `greyjoy-rebellion` | 27 | 13 | the real hub — event.war w/ PART_OF battle children |
| **D3 Greyjoy's Rebellion (stub)** | `greyjoys-rebellion` | 7 | 0 | **DUP** — thin stub, 7 inbound only; merge into the rich one |
| **D4 Riot of King's Landing** | `riots-in-kings-landing` | **1** | 0 | essentially **unbuilt** — highest salience-per-thinness |
| **D6 Tourney at Harrenhal** | `tourney-at-harrenhal` | 32 | 7 | RR S133 already touched it; theory-adjacent (gated) |
| **D6 Defiance of Duskendale** | `defiance-of-duskendale` | 11 | 0 | backstory; theory-adjacent |
| **C1 Varys** | `varys` | 65 | 1 | thinnest-causal major manipulator |
| **C2 Petyr Baelish** | `petyr-baelish` | 121 | 1 | huge social degree, **near-zero causal** typing |
| **C3 Bloodraven / Brynden Rivers** | `brynden-rivers` | 26 | 1 | **stub vs lore-weight**; Matt-flagged; D&E overlay |
| **C4 Euron** | `euron-greyjoy` | 52 | 0 | Kingsmoot S157 already enriched the social layer |
| **B5 Antler Men (a)** | `antler-men` | 4 | 0 | **DUP** with (b) |
| **B5 Antler Men (b)** | `the-antler-men-conspiracy` | 4 | 0 | **DUP** — resolve before wiring |
| **B6 Ice** | `ice` | 7 | 0 | REFORGED_INTO → oathkeeper + widows-wail **already exist** |
| **B6 Widow's Wail** | `widows-wail` | 2 | 0 | very thin |
| **B6 Oathkeeper** | `oathkeeper` | 5 | 0 | — |
| **B8 Lancel** | `lancel-lannister` | 37 | 0 | NOT thin; only the targeted `AGENT_IN death-of-robert` edge missing |
| **B8 Robert's death** | `death-of-robert-baratheon` | 6 | 1 | strongwine whodunit hub |

### Stale notes in `enrichment-coverage-plan.md` corrected this session
1. **B6 REFORGED_INTO is NOT "0 instantiations" anymore.** Graph-wide there are now **2** (`ice→oathkeeper`,
   `ice→widows-wail`). The "first-ever REFORGED_INTO showcase" rationale is obsolete → B6 demoted to a thin
   artifact-quote enrichment (widows-wail=2 is the thin bit), not a marquee.
2. **B5 Antler Men is a DUP** (`antler-men` + `the-antler-men-conspiracy`, both deg-4). Resolve the dup
   first; it's a prerequisite, not part of the dip's value.
3. **D3 Greyjoy's Rebellion dup is still live** (`greyjoys-rebellion` stub + `greyjoy-rebellion` rich/13-causal).
   The rich hub is already partly spined; the dip = merge the stub + add the missing marquee beats.
4. **Density drift** (all grew via the arc round): Varys 59→**65**, Petyr 109/5→**121/1**, Bloodraven 19→**26**,
   Euron 43→**52**. The *causal* counts stayed ~1 or 0 across the manipulators — social web is built, causal
   typing is the residual.

---

## RANKED granular-dip list

> **Sequencing reminder (Matt S130/S131):** within the granular tier everything matters — no single hard
> "#1"; pick by readiness × demand. Character webs (Class C) come LAST because most are already built as arc
> by-products. Ranked by **reader-salience × current-thinness × cross-arc payoff × readiness.**

### Group 1 — DO FIRST (high salience, ready, high cross-arc payoff; hub exists → WIRE+ENRICH, not build)

1. **D2 — The Hand's Tourney** (AGOT). `the-hands-tourney` has a rich 33-edge roster but **0 event-beats /
   0 causal** — the perfect Class-D profile (attach points ready, spine absent). Mint the marquee beats
   (Loras-unhorses-Gregor · Gregor-beheads-his-own-horse-&-attacks-Loras · the-Hound-saves-Loras · the
   melee · Littlefinger's bets) + role/causal wiring. Feeds the Gregor/Sandor/Loras/Renly webs; pairs with
   the Robert-Strong (B2, done) / Clegane material. **Recommended top pick** — biggest payoff for a
   no-build dip.

2. **D3 — Greyjoy's Rebellion** (289 AC). Load-bearing backstory hub joining Iron Islands + Starks +
   Baratheons + Lannisters. `greyjoy-rebellion` is partly spined (27/13). Dip = (a) **merge the
   `greyjoys-rebellion` stub** into it, then (b) add the missing marquee beats: burning of the Lannister
   fleet at Lannisport, the siege & storming of Pyke, **Theon taken hostage** (the root of his whole arc),
   Rodrik & Maron Greyjoy killed, the Robert+Ned+Stannis+Jaime+Balon roles. High cross-arc payoff (Theon
   arc root; Euron/Victarion backstory). **READY** (the merge is mechanical).

### Group 2 — HIGH VALUE, but a from-scratch spine BUILD (higher cost) — schedule deliberately

3. **D4 — The Riot of King's Landing** (ACOK). `riots-in-kings-landing` = **1 edge** — essentially unbuilt
   despite top reader-salience: the bread riots, the High Septon torn apart, **Sansa nearly raped & rescued
   by the Hound**, Tyrion struck, Lollys assaulted. A from-scratch spine build (so higher cost than D2/D3).
   Pairs with the Blackwater/KL cluster; extends the Sandor protective-arc thread.

### Group 3 — character-web residuals (Class C) — LAST per Matt; pick by demand

4. **C3 — Bloodraven / Brynden Rivers.** `brynden-rivers` stub (26/1) vs enormous lore weight. **Matt-flagged**
   (memory `project_bloodraven_enrichment_dip`) — but explicitly ONE of many, NOT a lead. The richest
   standalone-justified character dip: kin web (Bittersteel/Shiera/the Great-Bastard set), Raven's Teeth,
   Blackfyre wars, Hand tenure, the cave-mentor substrate (overlaps Bran A1.4, done S146). Unique asset:
   **D&E book-cite overlay** — the novellas (thk/tss/tmk) are readable directly (D&E Pass-1 is PARKED; do
   NOT un-park — read the chapter text for cites). **Theory readings stay GATED** — build the evidence
   substrate, not the readings.
5. **C1 — Varys.** Thinnest-causal major manipulator (65/1). The CONSPIRES_WITH / DECEIVES / COMMANDS_IN
   causal web across Ned/Tyrion/Cersei/Joffrey; the Aegon spy-network; the Rugen identity; Kevan-assassination
   motive. Pairs with **B5 Antler Men** + the (done) Ned black-cells.
6. **C2 — Petyr Baelish.** 121 deg but **1 causal** — the social web is built, the *causal/manipulation*
   typing is the whole residual (DECEIVES Ned/Lysa/Cersei/Olenna; the Vale plot; the S133 `murder-of-jon-arryn`
   SUSPECTED_OF properly anchored). Sansa/Vale (A2.2) was built S148, so the attach points exist.

### Group 4 — cheap targeted L2 fixes (interleave between the big dips; minutes each)

7. **B8 — Lancel `AGENT_IN death-of-robert-baratheon`.** Tiny, ready; completes the strongwine whodunit
   (Lancel is the operational hand; connects to `lancel MEMBER_OF warriors-sons`, S140). `lancel-lannister`
   is already dense (37) — this is a single targeted edge.
8. **B5 — Antler Men conspiracy.** **Resolve the dup first** (`antler-men` ↔ `the-antler-men-conspiracy`),
   then wire the conspiracy causally (Stannis's KL fifth column; feeds Varys C1). Small.

### Group 5 — DOWNGRADED / GATED / not-a-dip

9. **B6 — Ice → Widow's Wail + Oathkeeper.** DOWNGRADED: REFORGED_INTO already instantiated (2 edges). Now
   only thinness/quote enrichment (widows-wail=2). Low urgency; fold into a Tywin's-death pass-2 if ever.
10. **C4 — Euron.** 52/0; Kingsmoot S157 already enriched the social layer. Residual = artifact web
    (Dragonbinder) + the Bloodraven-parallel thread, which is **theory-adjacent → gated**. Low urgency.
11. **D6 — Rebellion prelude** (Defiance of Duskendale → Tourney at Harrenhal). Theory-adjacent (Lyanna/R+L);
    RR S133 already touched `tourney-at-harrenhal` (32/7). Evidence edges only, readings gated. Low priority.
12. **NOT A DIP — Blackwater named-ship `WIELDED_IN` roster** (~20 ships, acok-davos-03:47). Deterministic
    **Python batch** (artifact nodes exist with empty edges). Flagged since S139. Run opportunistically; do
    NOT spend a reasoning dip on it.

---

## Recommended sequence

1. **D2 Hand's Tourney** (no-build WIRE+ENRICH, top payoff) →
2. **D3 Greyjoy's Rebellion** (merge dup + beats; Theon-arc root) →
3. interleave the cheap fixes **B8** + **B5** (minutes each) →
4. **D4 Riot of KL** (the one big from-scratch build) →
5. the Class-C residuals **C3 Bloodraven** → **C1 Varys** → **C2 Petyr** (characters last) →
6. clean up B6 / C4 / D6 only if a neighbouring pass touches them; run the ship-roster Python batch
   opportunistically.

**The one real decision for Matt:** start with **D2 (Hand's Tourney)** as the first granular dip [recommended —
ready, no build, iconic], or lead with **D3 (Greyjoy's Rebellion)** for the higher cross-arc/backstory payoff
(it carries a mechanical dup-merge first). Both are Group-1; either is a fine opener.

---

## Scope cards — top 2

### D2 — The Hand's Tourney  [RECOMMENDED FIRST]
- **Built:** `the-hands-tourney` hub w/ 26 FIGHTS_IN + 6 ATTENDS roster + 1 LOCATED_AT (King's Landing).
  **Zero event-beats, zero causal edges.**
- **Missing:** the marquee beat-nodes — Loras-unhorses-Gregor (the mare-in-heat trick) · Gregor-beheads-his-
  own-horse-&-attacks-Loras · the-Hound-saves-Loras (the Hound/Gregor enmity beat) · the melee · the archery/
  Anguy. SUB_BEAT_OF wiring to the hub + AGENT_IN/VICTIM_IN/WITNESS_IN roles + Littlefinger's-bets thread.
- **Scale:** Med (≈4–6 beat-nodes, ~25 edges). **Dependency:** none (hub + roster ready). **Kind:** Class-D
  WIRE+ENRICH (no build). **Source:** AGOT (agot-sansa / agot-eddard chapters). whodunit-light, character-rich.

### D3 — Greyjoy's Rebellion  [higher-payoff alternate]
- **Built:** `greyjoy-rebellion` (27/13, event.war w/ PART_OF battle children). **Plus a thin dup**
  `greyjoys-rebellion` (7 inbound).
- **Pre-req:** merge `greyjoys-rebellion` → `greyjoy-rebellion` (loser→same_as redirect, survivor absorbs the
  7 inbound; the S126 `mutiny-at-castle-black` merge pattern).
- **Missing:** burning of the Lannister fleet at Lannisport · siege & storming of Pyke · **Theon-taken-hostage**
  (Theon-arc root; wire forward to his ACOK turn) · Rodrik & Maron Greyjoy killed · the Robert/Ned/Stannis/
  Jaime/Balon/Euron/Victarion roles.
- **Scale:** Med–Large (dup-merge + ~3–5 beats, ~25 edges). **Dependency:** dup-merge (mechanical).
  **Kind:** Class-D WIRE+ENRICH. **Source:** backstory in AGOT/ACOK Theon & Greyjoy chapters + wiki.

---

*Census inputs: direct `graph/edges/edges.jsonl` scan (deg + causal-degree per candidate) + `graph-query.py`
this session, S168. No subagent lenses were needed — the grounding is deterministic and the salience read is
series-knowledge.*
