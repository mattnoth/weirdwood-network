# Enrichment Ledger — running list (to-do / in-progress / done)

> **What this is.** The single running list of enrichment work: what's been done, what's in
> progress, what's queued. **Enrichment = second-pass deepening of an already-built unit** —
> adding the braided side-plots, secondary-character sub-arcs, contemporaneous "revelation"
> events, descriptive/quote/object depth, and unproven-but-load-bearing edges that weren't on
> the first-pass spine.
>
> **Created 2026-06-20 (S116)** as the arc-enrichment backlog; **broadened to a full ledger
> 2026-06-22 (S130, Matt)** to cover three UNIT kinds and to track status, not just queue work.

## The scope model — why we enrich EVENTS, not "containers" (codified S136, Matt)

> Read this first if "are we enriching WO5K, or Red Wedding, and why aren't those the same scale?"
> ever confuses you again. It confused us in S136 — this section is the answer.

**The unit of enrichment is the event-arc (a node + its edge-chain), NOT the container.** This is not a
preference — it falls out of two earlier structural decisions that leave nothing else to grab:

1. **No umbrella / parent nodes** (DECIDED S105/S106, `project_narrative_arc_reification`). An "arc" is a
   *chain of CAUSES/TRIGGERS/MOTIVATES edges* between event nodes. There is **no `war-of-the-five-kings`
   node**, no super-node for any arc.
2. **A "container" is a frontmatter TAG, not a node** (DECIDED S121, `project_containers_field_and_query_modes`).
   `red-wedding` carries `containers: [wo5k]`; `--container wo5k` is **bag-retrieval** over the tagged event
   nodes. WO5K/Essos/North/Aegon/Bran are **labels stamped on bags of events**, not objects.

→ So "enrich WO5K" has **no object to point a dip at.** The only things that physically exist on disk to
deepen are **event nodes and the edges between them.** The **event-arc is the largest graspable object**;
everything above it (a container, "the WO5K arc") is an abstraction — a tag or an edge-chain, not a thing.
We never chose "event over container"; the container was never a grabbable option.

**What is notated WHERE (the S136 question):**
- **Container *membership* IS in the graph** — the `containers:` frontmatter tag on each event node, queried
  via `--container`. Live tags (S136): wo5k 33 · essos 26 · north 19 · bran 13 · aegon 12 (+ a stray `jon` 4,
  a North-build leak, not an approved container — cleanup item).
- **The *canon list* "these 5 ARE the major containers" is NOT a graph object** — no registry node. It lives
  only in `worklog.md` Active Decisions (SET=5, S122) + memory. The graph knows *which nodes are in wo5k*; it
  does **not** contain a claim that *wo5k is a major container*. That's planning state.

**The descent has THREE granularity levels** (`Sequencing — the descent`, below). The level-1/level-2 line is
where S136 tripped:
- **Level 1 — major arcs** = event-arcs: *Robert's Rebellion, Red Wedding, Purple Wedding, Ned's-downfall,
  Blackwater, Tywin's-death, Cersei's-downfall, Brienne→Stoneheart, Sack-of-KL.* ← **L1 ROUND COMPLETE (S142,
  9 dips incl. the Sack double-dip).** Next = the L2-granular PLANNING session (below). (These are small next to
  "WO5K," but they are the TOP level — because they are the graspable objects.)
- **Level 2 — granular sub-plots WITHIN one arc** = the threads *inside* a level-1 event. Inside Ned's-downfall:
  gold-cloak bribery mechanics, the throne-room massacre of Stark guards, Littlefinger's maneuvering. Inside the
  Red Wedding: the Frey-pies / GNC layer. **"Granular" = smaller than an event-arc, not the event-arc itself.**
- **Level 3 — individual characters** (maybe, last).

**Multi-pass is real AND has two senses** (don't fuse them): (a) a *single event* can be enriched repeatedly
(RR/RW/PW all log pass-2 candidates); (b) "WO5K needs many passes" means WO5K has *many events*, each getting
its own dip. Both are true at once.

**Lens 4 is how the container-level connective tissue gets built — node-by-node, not by tag.** Lens 4
(existing-node↔existing-node causal-wiring) finds real causal edges between two already-built nodes that no
topic-lens owned. It is **cross-NODE, agnostic to container boundaries** — it fires both *within* a container
(`the-rains-of-castamere TRIGGERS red-wedding`, both wo5k) and *across* containers (`exile-of-jon-connington
ENABLES aegon-revealed` = RR→AEGON; `roberts-rebellion MOTIVATES robert-orders-daenerys-assassination` =
RR→Essos). The cross-container seams are the high-value ones (they wire dead-end arcs into the rest of the
graph). So the "deepen the whole theater's connective tissue" instinct **is** being served — accreted one dip
at a time through lens 4, instead of in one container-wide pass.

## STATUS: enrichment PHASE is OPEN (gate tripped S130)

The S116/S117 gate was "enrichment opens once Essos is spine-built AND WO5K #3/#4/#5 are built."
**As of S130 ALL 5 approved containers are spine-complete** (essos S119–120 · wo5k S123 · north
S125–126 · aegon S128 · bran S130). The gate has tripped and then some — **enrichment is now the
primary track** (Matt S130: "clear low-value remainders, then enrichment dips"). The
`major-arc-backlog.md` DARK count is down to the deep-lore / theory long tail.

## Enrichment UNITS (Matt S130 — three kinds, not just arcs)

Enrichment isn't only arc/cluster-shaped. A unit is anything with a built skeleton worth deepening:

1. **Arc / cluster** — a built causal spine (the original S116 unit). e.g. Kingsmoot→Euron, Red Wedding.
2. **Major character** — deepen one character's connection web across/within containers. e.g. **Bloodraven**
   (kin, rivalry, office, artifact, D&E links), **Bran** (the greenseer arc), Euron, Littlefinger, Varys.
3. **Major event within a container** — deepen one load-bearing event's surrounding texture / participants /
   revelations. e.g. the Purple Wedding whodunit layer, the Red Wedding's Frey/Bolton sub-plots.

**Multi-pass per unit is expected, not one-and-done** (S116 lesson, reaffirmed S130): the same cluster /
character / event can be enriched repeatedly — each pass (fresh subagents + accumulated harvest finds +
newly-built neighbor units) yields new connections. Track the **pass number** per unit below.

### Sequencing — the descent (Matt S130, SHARPENED S131)

**One enrichment dip per session (Matt S131).** Enrichment is its own session each time — don't bolt it onto a
remainder/build session. The low-value remainders are now CLEARED (S131: AEGON Victarion-voyage + NORTH N6);
the next session opens the enrichment phase proper.

**The order is a top-down DESCENT, not a flat two-bucket split (Matt S131):**
1. **Major narrative arcs FIRST** — the big causal spines (Red Wedding, Robert's Rebellion, the Essos/Dany
   spine, the AEGON invasion, the WO5K, etc.). Deepen the arc as a whole before zooming in.
2. **THEN granular clusters / sub-plots WITHIN those arcs** — the braided side-plots, secondary-character
   threads, and revelation-events that hang off each major arc (e.g. within the Red Wedding: the Frey/Bolton
   mechanics; within Dorne: the Queenmaker informer mystery).
3. **THEN individual characters — maybe, and LAST** (Matt S131: "and then individual characters maybe?").
   The character phase is tentative and comes after the arc + sub-plot work, because by then most of a
   character's web is already built as a by-product of the arcs they appear in.

**"No lead" + a BROAD roster, not a Bloodraven focus (Matt S131):** within any level everything matters — no
single "#1." **Bloodraven is flagged but is one of MANY character candidates, NOT the focus** (Matt S131:
"bloodraven is flagged but there should be more characters so we don't focus solely on him"). The character
roster is wide — Jon Snow, Daenerys (the raw-importance heavyweights), Littlefinger, Varys, Tyrion, Cersei,
Jaime, Stannis, Bran, Euron, Bloodraven, and more. Pick the next unit by what's ready / what a dip shows
demand for, not by a standing favorite.

**A dedicated PLANNING session sits between the arc phase and the granular phase (Matt S130):** after the major
arc enrichments are done, run a session whose whole job is to *enumerate and scope the granular cluster/
sub-plot/character dip list*. The character/event entries below are **seeds**, not the final plan — by the
time the arc work is done we'll know far more about what each cluster actually needs, so the real granular list
gets built then. Full sequence: **low-value remainders [DONE S131] → major narrative-arc enrichments →
[planning session: scope the granular dip list] → granular clusters/sub-plots → individual characters (maybe)**
(D&E full-Opus Pass-1 batch slots in after the first enrichment passes).

> **Maximal meal capture = STANDING harvest-bar rule inside enrichment dips (Matt S137). NOT a separate pass.**
> Matt's "I want all meals, maximal, just ask and get full descriptions" + "any time anyone eats, incl. bark/
> starvation/no-food" was said **in the CONTEXT of the enrichment runs** — endorsing that the dip harvest
> captures lots of food. Keep the dip harvest bar WIDE-OPEN on food (split-the-bar, already in the dip
> prompts; bake the grim/starvation register into every dip's harvest snippet). The schema already supports
> "ask and get descriptions": `object.food` nodes (~75: bread, bowl-of-brown, lemon-cake, boar, pigeon…)
> accumulate EVERY occurrence in `## Narrative Arc` (per-book, verbatim + `chapter:line`) + `## Quotes`,
> indexed at `graph/index/foods/`. So "all meals" = the foods category; "full description of X" = that dish
> node's Narrative Arc.
>
> **DEFERRED (post arc-enrichment, Matt S137): a Python food-keyword GREP to scrape all chapters for meals.**
> IF we ever want true full-corpus meal coverage, the safe/cheap way is a **deterministic Python script** with
> a food-keyword list (dish names + eat/feast/supper/hungry/starv*/bread/meat…) grepping all 344 chapters →
> seed rows for attach — NOT an LLM sweep. **Deferred until the narrative-arc enrichment runs are done.** (My
> S137 "LLM sweep all 5 books as a dedicated session" framing was an over-extension Matt never asked for —
> RETRACTED. See the deferred todo in `working/todos.md`.)

---

## Ledger — enrichment passes per unit

> **Status is a COUNT, not a binary** (Matt S130). A unit is never "done" — it's "1 enrichment pass done,"
> "pass 2 done," "3 done," and can always take another (multi-pass is the norm). `0` = no deliberate pass yet
> (may carry incidental overlays from a spine build — noted). Increment the count + log the pass when one ships.

| Unit | Kind | Passes done | Last pass | Notes |
|------|------|:-----------:|-----------|-------|
| Kingsmoot → Euron | arc/cluster | **1** | S116 | +2 beat-nodes, +6 edges, +12 descriptive attachments, +1 edge type (`SUSPECTED_OF`), ~14 harvest pointers; + 3 bridge nodes minted-in-place. Pass 2 candidates: Crow's Eye voyages, dragonbinder, bastard sons. |
| Robert's Rebellion | arc/cluster | **1** | S133 | First major-arc enrichment (board-picked, unanimous A/B/C). +3 nodes (`knight-of-the-laughing-tree-incident`, `exile-of-jon-connington`, `murder-of-jon-arryn`) + 24 edges (22 board + 2 A/B-bonus; 1 junk `GUEST_OF` dropped, 1 ENABLES rejected at fresh-verify) + 4 book-cite overlays + alias fix. Wired the dead-end cluster FORWARD: **RR→AEGON** (`battle-of-the-bells CAUSES exile-of-jon-connington ENABLES aegon-revealed`) + **RR→WO5K** (`coronation ENABLES wedding-of-robert-and-cersei`). Jon-Arryn-murder reified (lysa AGENT_IN; petyr+cersei SUSPECTED_OF — the false in-world misdirection); R+L contested-agency `rhaegar SUSPECTED_OF abduction-of-lyanna`; Howland/Ned WITNESS_IN ToJ; wildfire-cache agents. Fresh-verify 6 CONFIRM/2 ADJUST/1 REJECT (dropped `wedding ENABLES death-of-robert` as agency-collapse — RR→WO5K death-link deferred to a properly-sourced MOTIVATES). 0 drift, 0 new types. **Pass 2 candidates:** RR→Essos seam (`exile-of-viserys-and-daenerys`, deferred to Essos enrichment); Tower-of-Joy interior (gated); the Knight-of-the-Laughing-Tree squire identities; `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY` vocab decision (Matt). |
| Bloodraven / Brynden Rivers | character | **0** | — | incidental S130 overlay only (cave-form appearance + self-id book-cite). Pass 1 = the D&E deep-connections dip (scope below). |
| Bran (greenseer arc) | character | **0** | — | incidental S130: 12 anchor quotes on the 8 new beats. Pass 1 = the journey-deepening dip (scope below). |
| AEGON cluster | arc/cluster | **0** | — | S129 prose-only harvest-consume (overlays onto jon-connington/aegon/varys) — not a full pass. |
| WO5K container | arc/cluster | **0** | — | needs MANY passes (Karstark/Frey/Bolton/Riverlands/westerlands). |
| Red Wedding | arc/cluster | **1** | S134 | Second major-arc enrichment (board-picked). +2 nodes (`grey-wind-killed-at-the-twins`, `edmure-taken-hostage-at-the-twins`) + 23 edges + 14 descriptive quote/appearance attaches. **Fixed the dead-end hub** (downstream 1→ traversing chain): RW→roose-warden→{stannis-march, fArya-wedding}; wired 2 causal islands — `ser-wendel-manderly-is-killed MOTIVATES wyman-...-davos` (the North-remembers seam) + `the-rains-of-castamere TRIGGERS red-wedding` (the massacre-signal text node, was edge-less); `red-wedding`/`edmure-hostage ENABLES siege-of-riverrun`. Planner/witness substrate: Lothar AGENT_IN/COMMANDS_IN, Bastard-Walder (`walder-rivers`) AGENT_IN camp, Edwyn/Smalljon/Greatjon/Merrett role edges, Catelyn WITNESS_IN robb-killed, Arya WITNESS_IN camp. **4th causal-wiring lens** added to the board (S133 A/B finding banked) — it produced the 2 island-fixes. Fresh-verify 3 CONFIRM/3 ADJUST (warden→fArya ENABLES→MOTIVATES T2; warden→stannis & rw→siege → T2; merrett AGENT_IN→PARTICIPATES_IN). 0 drift. **REJECTED at synthesis:** `blackfish-escapes-the-twins` node (factually wrong — Blackfish held Riverrun, never at the Twins); `red-wedding CAUSES guest-right`(concept, novel pattern→ATTACH_QUOTE); `roslin SUSPECTED_OF conspiracy` (overclaims coerced victim). **Pass 2 candidates:** Frey-pies/GNC layer, Riverrun-siege downstream, the bedding sub-beats, Manderly-hostage (Wylis) thread, Arya post-RW kill-list node. |
| Purple Wedding | arc/cluster | **1** | S135 | Third major-arc enrichment (board-picked — consensus of 3 advisors; only arc in all three top-3s). +0 nodes (edge-only pass) + 16 edges. **Lit the dead-dark hub** (was 0 causal): `death-of-joffrey-baratheon` now walks **18 edges downstream** (TRIGGERS littlefinger-smuggles-sansa + ENABLES wedding-of-tommen; the existing trial→Oberyn→Tywin→Cersei-imprisonment→GC-landing chain now hangs off the death). **Whodunit layer** (the marquee gap): `tyrion-lannister` + `sansa-stark` SUSPECTED_OF death-of-joffrey (in-world false blame; Olenna/LF stay the true AGENT_IN/COMMANDS_IN). `petyr-baelish MOTIVATES olenna-tyrell` (the framing-seed) + `littlefinger-brokers-tyrell-lannister-alliance ENABLES joffrey-sets-sansa-aside`. Witness substrate: 5 WITNESS_IN (sansa/tyrion/margaery/tommen/loras). Object layer (3 islanded artifact nodes wired first time): joffrey OWNS widows-wail + wedding-chalice; strangler + wedding-chalice WIELDED_IN the death. `killing-of-dontos-hollard` integrated SUB_BEAT_OF. Fresh-verify (independent Sonnet) **6 CONFIRM / 3 REJECT**: dropped `betrothal ENABLES death` (too distal/agency-collapse), `dontos-killing ENABLES smuggle` (TEMPORAL INVERSION — Dontos shot after Sansa aboard), `smuggle ENABLES petyr-lysa-wedding` (incidental co-location). Synthesis also caught the lenses conflating `tyrell-plot-revealed` (the Sansa→Willas plot, NOT the murder). 0 drift, 0 new types (132). +14 harvest rows. **Pass 2 candidates:** the deferred `silver-hairnet-of-sansa-stark` artifact node + `sansa-assumes-alayne-stone-identity` Vale-arc node; the Kettleblack triple-agent web; Dornish-succession (Myrcella) downstream seam; feast food-nodes. |
| Ned's downfall | arc/cluster | **1** | S137 | Fourth major-arc enrichment (board-picked S136, unanimous A/B/C). +12 edges, 0 new nodes (Renly-offer node backed out at fresh-verify). Wired the conspiracy/betrayal SUBSTRATE the spine lacked: **revelation engine** `ned-discovers-the-truth-of-joffrey-s-parentage ENABLES arrest-of-eddard-stark` (was causally islanded → now a 2-cause convergence with death-of-robert on the spine, walks via `--full-chain`); **hidden origin** `cersei-lannister SUSPECTED_OF death-of-robert-baratheon` (the strongwine — Robert's death's first Cersei-agency edge; never asserts murder); **hidden-architect DECEIVES trio** `petyr-baelish`/`varys`/`pycelle DECEIVES eddard-stark`; witness substrate `arya`/`varys`/`cersei WITNESS_IN execution` (both Stark daughters now wired; Varys+Cersei present & trying to stop Joffrey) + `high-septon OFFICIATES ned-confesses` (first-use OFFICIATES); throne-room massacre `janos-slynt KILLS varly` + `sandor-clegane KILLS cayn` + `cayn VICTIM_IN gold-cloaks-betray-ned`. Independent fresh-verify **11 CONFIRM / 1 ADJUST-kept / 2 REJECT**: DROPPED `varys-confirms ENABLES confession` (MISTARGET — narrow wine-reveal node ≠ confession cause, the Sansa threat is) + the whole Renly-offer node/edges (SEMANTIC INVERSION — an offer that happened can't be "prevented"; Ned prevented the *seizure*). Synthesis also DROPPED `gold-cloaks ENABLES cersei-orders-the-SLEEPING-guards-executed` (that node is an **AFFC Cersei I** event, not the AGOT guards — wrong book) + `littlefinger CAUSES arrest` (agency-collapse, constitutive). 0 drift, 0 invented types. Backup `_regrounding/edges-pre-neds-downfall-enrichment-2026-06-23.jsonl`. **Pass-2 candidates:** the black-cells island stays dark (mint a broader `varys-visits-ned-in-the-black-cells` or a sansa-threat node, then wire ENABLES→confession); the Renly-offer (needs a `ned-refuses-renly-s-offer` or seizure-that-never-happened node); `lancel-lannister AGENT_IN death-of-robert` (evidence split across non-adjacent lines); `sansa-warns-cersei-of-ned-s-departure` hidden-upstream beat; valyrian-dagger/catspaw node + WIELDED_IN. |
| Blackwater | arc/cluster | **1** | S138 | Fifth major-arc enrichment (S136 board's clean #2). +6 nodes (`wildfire-trap-on-the-blackwater`, `tyrion-s-sortie-at-the-king-s-gate`, `garlan-tyrell-routs-stannis-as-renly-s-ghost`, `sandor-clegane-deserts-the-kingsguard`, `joffrey-recalled-to-the-red-keep`, `blackwater-chain-boom` [object.artifact]) + 41 edges. Built the off-spine battle substrate the hub lacked (was hub + 2 empty plate-3 stubs → now 39 edges). **Marquee gap = the Renly's-ghost rout:** `garlan-tyrell-routs-stannis-as-renly-s-ghost CAUSES stannis-retreats-to-dragonstone` (+ garlan AGENT_IN / IMPERSONATES renly / KILLS guyard-morrigen Tier-2) wires Garlan's character node into the NORTH spine (walks 11 hops to Crofter's Village). **Tactical substrate:** wildfire-trap (tyrion+hallyne AGENT_IN; `wildfire`+`blackwater-chain-boom`+fury/black-betha/swordfish WIELDED_IN); the King's-Gate sortie (`sandor-deserts ENABLES sortie ENABLES a-knight-attacks-tyrion-s-shield`); `battle MOTIVATES sandor-clegane` (fire-fear). **Whodunit:** `cersei SUSPECTED_OF a-knight-attacks-tyrion-s-shield` (Tier-2, the Mandon-Moore attempt). **15 hub participant roles** (COMMANDS_IN tyrion/stannis/imry/bronn/tywin/mace/tarly; FIGHTS_IN sandor/davos/pod/balon/mandon/garlan/guyard; ilyn PARTICIPATES_IN) + `sansa WITNESS_IN` (sees the burning sky; **cersei WITNESS_IN dropped — text-anchor fail**). `podrick RESCUES tyrion`. **CRITICAL non-conflation:** the Blackwater wildfire got its own node, NEVER wired to `wildfire-plot` (the Aerys-283AC node). Fresh-verify **39C/1A/2R**: ADJUST `sandor-deserts CAUSES→ENABLES sortie` (Tyrion's free choice); DROP `sansa-aside ENABLES purple-wedding` (contested distal seam → PW pass-2); rest CONFIRM. 0 drift (41/41 quotes verify), vocab steady at 170. Backup `_regrounding/edges-pre-blackwater-enrichment-2026-06-23.jsonl`. 33 harvest rows pushed (full pre-battle/ballroom menus, descriptions, the Gentle Mother song, ship-roster Python-batch candidate). **Pass-2 candidates:** the Antler Men wiring (needs member nodes / clearer event model); battle-of-oxcross/battle-of-the-fords ENABLES (WO5K seams, inference-grounded → WO5K enrichment); `tyrion-loses-the-handship` node + Tywin/battle CAUSES it; the full named-ship WIELDED_IN roster (~20, Python batch); the `Gentle Mother` object.text song node + Sandor's-white-cloak artifact; the sansa-aside→Purple-Wedding seam (PW pass-2). |
| Tywin's death | arc/cluster | **1** | S139 | Sixth major-arc enrichment (Fork-1 board pick, Matt S139). +5 nodes (`tywins-crossbow`, `hands-chain-of-office`, `oberyn-spear` [object.artifact]; `shae-testifies-against-tyrion-at-trial`, `varys-smuggles-tyrion-out-of-kings-landing` [event.incident]) + 34 edges. Built the OFF-SPINE substrate the S109 spine lacked: **the murder instruments** (Tyrion kills Tywin with his OWN wall-hung crossbow — OWNS+WIELDS+WIELDED_IN+KILLED_WITH; strangles Shae with the Hand's gold chain — WIELDS+WIELDED_IN+KILLED_WITH; Oberyn's 8-ft ash spear WIELDED_IN the combat); **the marquee cross-arc seam** `murder-of-elia... MOTIVATES oberyn-martell` (wires the Sack-of-KL arc into Tywin's death — Oberyn champions Tyrion to reach Gregor); **the Tysha deception** `tywin DECEIVES tyrion` (by_lie); **the instrumental seam** `tyrion-kills-shae ENABLES assassination` (the bedchamber detour gave him the crossbow — now a `--full-chain` precondition hop, 12 chain edges); **Shae's betrayal-testimony** reified (SUB_BEAT_OF trial + cersei COMMANDS_IN + MOTIVATES tyrion → trial-by-combat); **the escape→exile** (jaime-frees ENABLES varys-smuggles, forward-wires the ADWD arc); **trial hub** lit from a thin node to 15-in (mace+oberyn judges PARTICIPATES_IN, cersei COMMANDS_IN, 8-witness parade PARTICIPATES_IN); combat roles (oberyn+gregor FIGHTS_IN, ellaria WITNESS_IN). **THE LINE-CHECK CATCH:** lenses mis-cited Shae's testimony / "my giant of Lannister" to ch09:39 — it's ch10 (she's the "one final witness"). Fresh-verify **6C/5A/1R**: DROPPED `oberyn POISONS gregor` + `manticore-venom WIELDED_IN` (ASOS leaves the poison unconfirmed — "Oil? Or poison? Tyrion decided he would sooner not know"; "manticore" never in ASOS → defer to AFFC/Gregor dip) + `shae-testifies CAUSES kill` (agency/redundant with the spine `jaime-reveals CAUSES kill` + the MOTIVATES route); re-cited the Elia-motive ch09:399→ch10:187. 0 drift (34/34 verify), first-use `KILLED_WITH` (live types 133→134, locked vocab). Backup `_regrounding/edges-pre-tywin-death-enrichment-2026-06-23.jsonl`. **Pass-2 candidates:** Oberyn POISONS gregor + manticore-venom (AFFC/Gregor dip where the venom is named); `the-strangler` concept.medical node + Pycelle's pharmacopoeia; Tommen-accession node (Cersei-arc); Jaime-burns-Cersei-letter (Jaime-arc); `jaime DECEIVES tyrion` companion edge; the Ice/Widow's-Wail/Oathkeeper reforging overlay. |
| Sack of KL | arc/cluster | **1** | S142 | Ninth major-arc enrichment (Matt S142 — chose the Sack double-dip over the L2-granular planning session). The flagged low-yield double-dip: hub was already dense (4 sub-beats + full atrocity/whodunit layer from RR S133 + Elia→Oberyn S139). +2 nodes (`tywin-presents-bodies-to-robert`, `jaime-found-seated-on-the-iron-throne` [event.incident]) + 17 edges. **WILDFIRE INTEGRATION** — `wildfire-plot ENABLES aerys-commands-the-city-burned` (the caches are the precondition; the burn-order had only 1 inbound); the two un-wired pyromancers `belis`/`garigus` AGENT_IN wildfire-plot (Rossart already wired); `qarlton-chelsted VICTIM_IN wildfire-plot` + `aerys KILLS chelsted` (the Hand burned for opposing). **PYROMANCER-HUNT** `jaime KILLS belis`+`garigus` (jaime KILLS rossart/aerys already existed). **TWO ICONIC AFTERMATH BEATS**: `tywin-presents-bodies-to-robert` (SUB_BEAT_OF sack; tywin AGENT_IN; robert WITNESS_IN — "I see no babes. Only dragonspawn" Robert-complicity) + `jaime-found-seated-on-the-iron-throne` (SUB_BEAT_OF the slaying; jaime AGENT_IN; **eddard WITNESS_IN — the gate-passing beat** [Ned witnessed the throne-tableau, NOT the killing]; roland-crakehall WITNESS_IN the slaying itself). **MARQUEE cross-arc seam** `wildfire-plot ENABLES wildfire-trap-on-the-blackwater` (T2 — TEXT-DIRECT via the Dragonpit cache acok-tyrion-11:107, "King Aerys's fickle fruits" acok-tyrion-13:19; S138 kept the NODES separate, this wires the recovered-caches thread WITHOUT conflating) + `murder-of-elia MOTIVATES doran-reveals-fire-and-blood-pact` (T2, the 17-yr Dornish long-game — "Vengeance. Justice. Fire and blood."). Fresh-verify (independent Sonnet) **15C/2A/0R**: DROPPED `tywin-presents ENABLES coronation` (over-distal/redundant with `sack CAUSES coronation`); DOWNGRADED the Blackwater seam T1→T2 (cross-book deduction). 0 drift (17/17 verify, clean line-check — no self-inflicted slips), 0 invented types (vocab 170). Backup `_regrounding/edges-pre-sack-kl-enrichment-2026-06-24.jsonl`. 14 harvest rows pushed. **THEORY-GATED (not minted):** the Aegon babe-swap (Varys/fAegon) — existing slugs used as-is, no swap-claim. **Pass-2 candidates:** the visceral kingslaying quote → slaying node ## Quotes (it has none); the wildfire-cache-locations overlay; Ser Elys Westerling WITNESS_IN the throne-scene; the murder-of-elia → Doran/Dornish-vengeance downstream (Quentyn/Aegon-claim); Jaime's "Kingslayer" reputation as a queryable concept. |
| Cersei's downfall | arc/cluster | **1** | S140 | Seventh major-arc enrichment (Fork-1 board pick, Matt S140). +3 nodes (`maggy-the-frogs-prophecy` [concept.prophecy]; `murder-of-the-old-high-septon`, `cersei-resolves-on-trial-by-combat` [event.incident]) + 15 edges. Built the OFF-SPINE substrate the S114 spine lacked: **the hidden MOTIVATES engine** — Maggy the Frog's valonqar/younger-queen prophecy (PROPHESIED_BY maggy + MOTIVATES cersei + cersei SUBJECT_OF_PROPHECY + FORESHADOWS the capture), the psychological driver behind the whole anti-Margaery campaign; **the Kettleblack backstory crime** `murder-of-the-old-high-septon` (osney AGENT_IN; **cersei COMMANDS_IN** — NOT SUSPECTED_OF: her own POV at ch10:247 "I'll rid myself of this High Septon just as I did the other" authorially confirms the order; ENABLES the rearming via the off-node High-Sparrow election); **de-islanded** `cersei-fills-in-the-arrest-warrants` (was 0 causal → `blue-bard-arrest ENABLES warrants`, the bard's coerced names at ch09:199 literally fill the warrants); **fixed the dead-end** (`cersei-is-stripped-and-imprisoned` had 0 downstream → `CAUSES cersei-resolves-on-trial-by-combat`, the Jaime-plea/Robert-Strong-champion hinge to ADWD, now terminating a 16-hop chain back to the poisoned hairnet) + qyburn ADVISES cersei. Secondary substrate: qyburn TORTURES blue-bard, taena INFORMS + CONSPIRES_WITH cersei, lancel MEMBER_OF warriors-sons (book-grounds the wiki SWORN_TO). Fresh-verify (independent Sonnet) **15 CONFIRM / 0 ADJUST / 0 REJECT** (the synthesis line-checking pre-empted the usual catches). 0 drift (15/15 verify), 0 invented types (locked 170-vocab); first-use-in-graph `FORESHADOWS` + `INFORMS` (in-use 134→136). Backup `_regrounding/edges-pre-cersei-downfall-enrichment-2026-06-23.jsonl`. **Dropped at synthesis (dedup):** `cersei LOVER_OF osney` / `orton AGENT_IN bard-arrest` / `cersei FEARS tyrion` (all already in graph). **Pass-2 candidates:** `aurane-waters-deserts-with-the-fleet` node; `creation-of-robert-strong` (Robert-Strong/Gregor character unit); `kevan-assumes-the-regency` (ADWD); the Senelle/Falyse→Qyburn SUSPECTED thread. |
| Brienne → Stoneheart | arc/cluster | **1** | S141 | Eighth major-arc enrichment — the LAST clean L1 arc (Matt S141). +3 nodes (`hound-helm` [object.artifact]; `ambush-at-crossroads-inn`, `fight-at-the-whispers` [event.battle]) + 39 edges. The AFFC S115 spine was a 2-edge dead-ended chain; the character layer was dense (Brienne 73 edges) but the EVENT nodes were thin/islanded. **THE MARQUEE FIX: de-islanded `raid-on-saltpans`** (had 0 participant edges → now 3 upstream + 1 downstream via `--full-chain`): rorge/biter AGENT_IN, brave-companions + capture-of-harrenhal ENABLES, LOCATED_AT saltpans, the Elder Brother's grave-helm "grievous error" ENABLES, raid MOTIVATES brienne's hunt, randyll-tarly DECEIVES the brotherhood (counter-rumor). **The hound-helm misattribution engine** (Sandor OWNS → Rorge LOOTED_BY → WIELDED_IN Saltpans+inn → Lem LOOTED_BY off the corpse) — first-use-in-graph `LOOTED_BY` (×2; was a defined-but-never-instantiated type → in-use 0→2; vocab steady 170). **Two new event hubs**: the inn ambush (Brienne kills Rorge, Biter maims her, Gendry kills Biter → `CAUSES brienne-brought-before-lady-stoneheart`, giving the tribunal node a 2nd causal route in) + the Whispers fight (Brave-Companions remnant; shagwell KILLS dick-crabb). **Cross-arc seam** `red-wedding MOTIVATES catelyn-stark` (ASOS RW → AFFC antagonist) + catelyn MOTIVATES lem. **Dead-end fix**: `brienne-brought-before-lady-stoneheart MOTIVATES brienne-tarth` (the sword-or-noose ultimatum → her screamed word) — honest de-dead-end WITHOUT a fabricated hanging-death node. SLUG TRAPS corrected (lenses used non-existent thoros-of-myr/septon-meribald/nimble-dick-crabb; baseline mis-named BWB Lem as lem-standfast → real node `lem`). Fresh-verify (independent Sonnet) **37C/3A/0R**: DROPPED `quincy-cox WITNESS_IN raid` (present-but-shielded — he barred his gates & hid; "saw from battlements" is wiki-only → fails the WITNESS_IN text-anchor gate); downgraded `randyll DECEIVES` T1→T2 (hearsay anchor). 0 drift (39/39 verify after fixing 4 self-inflicted line-check slips: 1 ellipsis splice + 1 comma→period + 2 attribution-splices). Backup `_regrounding/edges-pre-brienne-stoneheart-enrichment-2026-06-24.jsonl`. 22 harvest rows pushed (full Quiet-Isle/Meribald meals, the road-of-hanged-men salt-in-mouths, the broken-men sermon). **NOT minted (over-read/scope):** Sandor's death (`DIED_AT/BURIED_AT quiet-isle` — the gravedigger-lives subtext; → Hound/Sandor character unit); `brienne-pod-hyle-hanged` (asserting the hanging-death is false — Brienne survives; the cliffhanger stays a cliffhanger). **Pass-2 candidates:** the Sandor-death/gravedigger cluster + stranger/driftwood horse (Hound unit); merrett-frey-hanging + the salt-in-mouths hanging-campaign node (Stoneheart-vengeance / RW-aftermath); "Mad Dog of Saltpans" alias-add to sandor-clegane. |
| Dorne / Myrcella (Queenmaker) | arc/cluster | **0** | — | 19 harvest rows pushed S117. |
| Essos clusters | arc/cluster | **0** | — | Slaver's Bay/Meereen sub-plots; Fire-and-blood reveal. |
| Euron | character | **0** | — | + the gated Euron↔Bloodraven evidence thread (scope below). |
| Jon Snow · Daenerys | character | **0** | — | heavyweight character units (huge cross-container webs) — character phase. |
| Purple Wedding whodunit · Red Wedding Frey/Bolton mechanics | event | **0** | — | event-unit candidates. |

*(The detailed next-pass scope for the Matt-flagged units follows; the table above is the at-a-glance count.)*

---

## Next-pass scope — character units (broad roster — comes LAST, after arcs AND their sub-plots; Matt S131)

> **Characters are the LAST level of the descent and tentative** ("individual characters maybe?", Matt S131).
> Most of a character's web gets built as a by-product of the arc + sub-plot enrichments they appear in, so the
> dedicated character phase is for what's left. **Bloodraven is ONE of many, not the focus** — the roster is wide
> (Jon, Dany, Littlefinger, Varys, Tyrion, Cersei, Jaime, Stannis, Bran, Euron, Bloodraven, …). The Bloodraven
> hooks below are kept because they're concrete, not because he leads.

> No "lead" here (Matt S130). By raw importance the heavyweights are **Jon Snow** and **Daenerys** (each a huge
> cross-container web — queue them when the character phase opens). **Bloodraven, Bran, Euron** below are
> Matt-flagged specifics with concrete hooks, not a ranking. Also eventually: Littlefinger, Varys, Tyrion, etc.

### Bloodraven / Brynden Rivers — deep connections back through Dunk & Egg
**Matt S130: "we def need more bloodraven deep connections going all the way back to dunk and egg bc
bloodraven / brynden rivers big in theories."** Full scope + dedup baseline: memory
`project_bloodraven_enrichment_dip`. Builds the *evidence substrate* (Tier 1–2 connection edges) the
gated theories track was waiting on — **theory READINGS stay gated** (`project_theories_track_deferred`).
- Kin/rivalry: Bittersteel (Aegor Rivers, half-brother + nemesis), Daemon Blackfyre, Melissa Blackwood
  (mother), Aegon IV (father), the Great Bastards; enrich the existing `LOVER_OF shiera-seastar`.
- Office/political: Hand to Aerys I + regency; killed Aenys Blackfyre under guest-right → the Wall; Great
  Council 233; the thousand-eyes spy network.
- **D&E book-cite overlays** (no Pass 1 yet — read the novella files directly): `tmk/tmk-dunk-01.md` (on-page
  at Whitewalls, the Second Blackfyre plot, the Bittersteel capture) primary; `tss`/`thk` references.
- Artifacts/companies: Dark Sister (WIELDED), the weirwood longbow, the **Raven's Teeth** (COMMANDS).
- Wall/cave (some built S130): confirm `coldhands SERVES/SWORN_TO` points to `brynden-rivers` not the
  `three-eyed-crow` species node (S130 slug trap); children of the forest; mentor-to-Bran.

### Bran — the greenseer arc deepening
The S130 spine is built (8 beats). Enrich: the 4 still-open `bran-dip` harvest rows (Old Nan Long-Night
foreshadowing, weirwood-paste food node, cave floor-bones place, the becoming-a-weirwood foreshadowing) +
the research subagents' batchA/batchB rows; the Bran↔Jojen greendreaming dyad (D3, `working/dyad-queue.md`);
descriptive depth on the journey beats. Pairs naturally with the Bloodraven pass (shared cave cluster).

### Euron — incl. the Euron ↔ Bloodraven connection thread
**Matt S130: "theories that Euron is connected to bloodraven."** The Euron spine is built (Kingsmoot, S116).
Enrich Euron's own web (Crow's Eye voyages, the dragonbinder, the bastard sons) AND the textual Euron↔
Bloodraven links (the shade-of-the-evening / sorcery / "thousand eyes" resonances) **as evidence edges only**
— the theory that they're connected is a GATED reading, but the on-page links that fuel it are fair Tier-2
substrate. Surface to the theories track when it opens.

## Next-pass scope — arc / cluster units (these go first; multi-pass expected)
- **WO5K container** — needs MORE than one pass (Matt: "gonna need more than that treatment"): Karstark, Frey,
  Bolton, the Riverlands chevauchée, Robb's westerlands campaign.
- Red Wedding · Purple Wedding · Tywin's death · Blackwater · Ned's downfall · Robert's Rebellion · Sack of KL —
  each has side-plots not on its spine.
- Cersei's downfall + Brienne→Stoneheart (AFFC, S114/S115) — the Blue Bard, the Faith Militant's rise, the
  Brotherhood's hangings.
- **Dorne / Myrcella (Queenmaker, S117)** — the "Someone always tells" informer mystery; Arys Oakheart's
  seduction sub-arc; the conspirator dispersal (Drey→Norvos, Garin→Tyrosh, Sylva→Greenstone); Darkstar's escape
  (downstream-dark). 19 harvest rows pushed S117.
- **Essos clusters** — the Slaver's Bay / Meereen braided sub-plots; the Quentyn/Doran "Fire and blood" reveal
  (Essos-bridge seed).

## Next-pass scope — event units within containers
- Purple Wedding whodunit layer (the poisoner attribution — `SUSPECTED_OF` candidates).
- Red Wedding internal Frey/Bolton mechanics.
- (add as dips surface them.)

---

## ROADMAP — Dunk & Egg full Opus Pass-1 batch (Matt S130)

**D&E Pass 1 is being UN-DEFERRED.** Matt S130: "we can do Dunk And Egg full Opus analysis batch job soon …
cake compared to doing an analysis over a whole book, plus we have come so far since the first book passes, we
can def make those prompts better." So:
- **Scope:** the 3 novellas (THK/TSS/TMK), full Opus mechanical Pass 1 — small vs a full book.
- **Improve the prompts first:** the v3 Pass-1 prompt predates everything we've learned; revise before running
  (the "make those prompts better" step). The D&E extractions then feed the Bloodraven enrichment with proper
  structured nodes instead of book-cite-overlay-only.
- **RUN IT UNATTENDED via `longrun.sh` — and use it to TEST that machinery (Matt S130).** D&E is the ideal
  test payload for the unified worker script (`scripts/worker-template.py`) + `longrun.sh` supervisor (S97/S99;
  survives rate-limit walls, auto-resumes — cf. `scripts/stage4-run-forever.sh`, memory
  `project_stage4_run_forever_wrapper`): small, self-contained, mechanical. Write a D&E **sub-script** (worker
  config for the 3 novellas) and let longrun drive it. This **decouples D&E from the enrichment ordering** — it
  no longer has to wait for "after the first enrichment passes"; it can run **CONCURRENTLY / in the background**
  whenever Matt has spare usage or is away during the (interactive, one-at-a-time) enrichment runs. Two wins in
  one: get D&E extracted AND exercise the unattended-longrun pipeline that hasn't been run in a while.
  **Caveat:** per `feedback_no_extraction_without_asking`, confirm with Matt before launching any extraction.
- Today (before that batch): Bloodraven D&E links come via the **book-citation-overlay** pattern
  (`feedback_book_citation_overlay_value`) — read the novella files directly, attach `chapter:line` cites.

---

## A/B model experiment — Sonnet-lens board vs. max-effort Opus (S133, Matt-requested)

**Setup.** After shipping the RR pass via the standard machine (3 Sonnet lenses + Opus orchestrator synthesis +
Sonnet fresh-verify), we ran ONE max-effort **Opus** analyst doing the ENTIRE RR enrichment scope as a single
blind pass (deduped against `baseline.md` only; did not read the lens/synthesis files; treated the parallel-minted
nodes as non-existent). Proposal: `working/enrichment/rr/proposal-opus-ab.md` (51 items).

**Verdict — a MODEST but real difference; orchestration matters more than proposer-tier.**
- **~90% convergence on the high-value core.** Opus independently arrived at the SAME 3 new nodes (KotLT-incident,
  exile-of-jon-connington, murder-of-jon-arryn), the SAME RR→AEGON bridge, the SAME Jon-Arryn substrate
  (lysa AGENT_IN / petyr+cersei SUSPECTED_OF), the SAME ToJ witnesses, the SAME wildfire overlays, the SAME junk-drop
  and the SAME `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY` NEEDS_VOCAB hold. → **strong validation of the cheaper Sonnet board.**
- **Opus caught a real coverage SEAM the lens-division missed:** existing-node→existing-node causal edges that no
  single Sonnet lens "owned." Two were genuine, well-grounded, structural-gap fixes and were **minted as A/B bonus**
  (run_id `rr-enrichment-s133-ab`): **`roberts-rebellion MOTIVATES robert-orders-daenerys-assassination`** (gave the RR
  hub its FIRST real outgoing edge — the cluster head was a dead-end; also a clean RR→Essos seam) +
  **`wildfire-plot MOTIVATES slaying-of-aerys-ii-the-kingslaying`** (Jaime's stated motive for the kingslaying).
- **Opus was slightly NOISIER on dedup** (re-proposed 4 already-existing nodes; correct per its blind rule but it would
  have needed a synthesis pass to filter). Its rejection reasoning was strong (caught agency-collapse, Rhaegar-died-first,
  granularity overclaim) — comparable to our fresh-verify.
- **Caveat (not a clean RCT):** the Sonnet path had Opus orchestration + a fresh-verify layer; the Opus path was a raw
  single agent with neither. The honest lesson: **the model tier of the proposal agents is NOT the bottleneck — the
  orchestration structure (shared dedup baseline + holistic causal-wiring lens + fresh-verify) is.** The lens division
  itself created the only real gap, and a holistic causal pass (any tier) closes it. RECOMMENDATION for future dips: keep
  the cheap fanned-out board, but ADD one explicit "existing-node↔existing-node causal wiring" lens to the board so the
  seam doesn't recur (Opus-as-proposer is not required to get those edges).
- **Held for RR pass 2** (Opus-found, lower-priority / more interpretive): `murder-of-elia… MOTIVATES landing-of-the-golden-company`
  (Tier-2, the survival-claim premise — wants fresh-verify); trident book-cite overlay (Robert "drove the spike… into his
  black heart", agot-eddard-10:171); `lyanna LOCATED_AT tower-of-joy`; atrocity-node AGENT_IN re-targeting.

## The enrichment-pass machine (smoke-tested S116)

1. **Fan out 2–3 fresh subagents, each a different lens** on the built unit:
   - secondary-character sub-arcs (the braided side-POVs),
   - thread/revelation + contemporaneous events + any unproven-but-load-bearing claims,
   - descriptive/quote/object depth (the "what does X look like" layer).
   Paste vocab + the harvest snippet; tell them PROPOSE-don't-mint + dedup-check every node.
2. **Synthesize + decide** what's worth minting vs deferring (forward-dangling cross-book nodes defer).
3. **Verify every cited line against the files** (subagents reconstruct quotes — always check),
   mint nodes/edges via a `scripts/mint_<unit>_enrichment.py` (backup + re-run guard),
   **fresh-verify the interpretive edges**, stamp, rebuild derived artifacts.
4. **Consume the harvest pointers** the dip refilled.

## Enrichment yield is real (S116 evidence)

One already-harvested cluster → **+2 beat-nodes, +6 edges, +12 descriptive attachments, +1 new edge type
(`SUSPECTED_OF`), ~14 fresh harvest pointers**, almost no overlap with the first harvest pass. The hypothesis
("a cluster can be enriched several times and keep yielding") held.

## Process rules
- Forward-dangling cross-book nodes **defer to the downstream container's enrichment**, not minted into a void.
  (S116 refinement: a node is only forward-dangling if its UPSTREAM is missing; if upstream exists, mint now.)
- Interpretive/causal enrichment edges get the same **fresh-subagent verify** as spine edges.
- `SUSPECTED_OF` (S116) is the type for unproven-but-load-bearing agency (Tier-2, never asserts the act).
  Reuse for Jon Arryn's murder, Joffrey's parentage, the Purple Wedding poisoner, etc.
- **Theory READINGS stay gated** (`project_theories_track_deferred`); enrichment builds the Tier-1/2 evidence
  substrate those theories will later traverse, but does not assert the theory.
- "Log it for later" is the same fragile deferral as parking a node — if you have the verbatim quote + a valid
  home NOW, attach it now. The only true deferrals are missing-upstream or missing-source.
